from flask import Flask, request, render_template
import sqlite3
import openai
from math import ceil
import pandas as pd
import joblib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)
# OpenAI API 키 설정
#openai.api_key = ""
# OpenAI API 키를 입력하세요.

async def answer(prompt):
    # OpenAI GPT 모델 호출
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o",  # 최신 "gpt-4-turbo" 모델 사용
        messages=[
            {"role": "system", "content": "당신은 한국어로 차량을 고객에게 간단하게 설명해주는 전문 중고차 설명가 입니다. 최종적으로 고객에게 가격이 합리적인지를 알려주는 역할입니다. 문장이 끝날때 마다, 줄넘김 (<br>)을 사용해서 읽기 쉽게 구어체로 사용자에게 설명해주세요"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,  # 응답의 최대 토큰 수
        temperature=0.8,  # 텍스트 다양성 조정 (0.7은 적당한 창의성)
    )

    # 생성된 텍스트 추출
    review = response["choices"][0]["message"]["content"].strip()
    return review

# 차 데이터 스크래핑 및 가격 계산 함수
def crawling(id):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_options)
    # https://www.encar.com/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid=37896036
    dummy = list(1 for i in range(0, 17))
    url = f"https://www.encar.com/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid={id}"
    driver.get(url)

    try:
        name_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//th[text()='차명']/following-sibling::td"))
        )
        car_name2 = name_element.text.strip()
        # + 리콜대상
        labels_1 = ['튜닝', '특별이력', '용도변경', '리콜대상']
        for i, label in enumerate(labels_1):
            try:
                element = driver.find_element(By.XPATH,
                                              f"//th[text()='{label}']/following-sibling::td/span[contains(@class, 'txt_state on')]")
                if element.text.strip() in ["없음", "해당없음"]:
                    dummy[i] = 1
                else:
                    dummy[i] = 0
            except NoSuchElementException:
                dummy[i] = 1
            try:
                element = driver.find_element(By.XPATH,
                                              f"//th[text()='{label}']/following-sibling::td/span[contains(@class, 'txt_state active')]")
                if element.text.strip() in ["없음", "해당없음"]:
                    dummy[i] = 1
                else:
                    dummy[i] = 0
            except NoSuchElementException:
                dummy[i] = 1
        try:
            retag = driver.find_elements(By.CLASS_NAME, 'list_state')
            for tag in retag:
                find_tag = tag.find_elements(By.TAG_NAME, 'li')
                for rank in find_tag:
                    change = rank.text
                    if "후드" in change:
                        dummy[4] = 0
                    if "프론트 휀더(좌)" in change:
                        dummy[5] = 0
                    if "프론트 휀더(우)" in change:
                        dummy[6] = 0
                    if "프론트 도어(좌)" in change:
                        dummy[7] = 0
                    if "프론트 도어(우)" in change:
                        dummy[8] = 0
                    if "리어 도어(좌)" in change:
                        dummy[9] = 0
                    if "리어 도어(우)" in change:
                        dummy[10] = 0
                    if "라디에이터 서포트(볼트체결부품)" in change:
                        dummy[11] = 0
                    if "프론트 패널" in change:
                        dummy[12] = 0
                    if "프론트 휠하우스(좌)" in change:
                        dummy[13] = 0
                    if "프론트 휠하우스(우)" in change:
                        dummy[14] = 0
                    if "리어 휠하우스(좌)" in change:
                        dummy[15] = 0
                    if "리어 휠하우스(우)" in change:
                        dummy[16] = 0

        except NoSuchElementException:
            a = 1
        tuning = dummy[0]
        special = dummy[1]
        using = dummy[2]
        recall = dummy[3]
        hood = dummy[4]
        fh_left = dummy[5]
        fh_right = dummy[6]
        fd_left = dummy[7]
        fd_right = dummy[8]
        ld_left = dummy[9]
        ld_right = dummy[10]
        rs = dummy[11]
        fp = dummy[12]
        fhh_left = dummy[13]
        fhh_right = dummy[14]
        rhh_left = dummy[15]
        rhh_right = dummy[16]

        # 드라이버 종료 및 결과 반환
        driver.quit()
        return tuning, special, using, recall, hood, fh_left, fh_right, fd_left, fd_right, ld_left, ld_right, rs, fp, fhh_left, fhh_right, rhh_left, rhh_right
    except Exception as e:
        driver.quit()
        print(f"Error occurred while processing car data: {e}")
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

# 해외차 모델 가져오기 (류건)
def get_models_for_outcountry():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 카테고리별 해외차 제조사 목록
    foreign_categories = {
        '독일': ['BMW', '벤츠', '아우디', '폭스바겐', '포르쉐', '마이바흐', '마세라티', '미니', '벤틀리', '롤스로이스'],
        '일본': ['닛산', '도요타', '마쯔다', '렉서스', '미쯔비시', '스바루', '스즈키', '혼다'],
        '미국': ['링컨', '닷지', '람보르기니', '맥라렌', '머큐리', '사브', '애스턴마틴', '어큐라', '인피니티', '재규어', '지프', '캐딜락', '크라이슬러', '테슬라', '페라리', '포드', '푸조', '피아트', '험머'],
        '중국': ['동풍소콘', '북기은상'],
        # 필요하다면 카테고리 재조정과 제조사 목록 수정
    }

    models_by_category = {}
    for category, manufacturers in foreign_categories.items():
        category_data = {}
        for manufacturer in manufacturers:
            query = "SELECT DISTINCT model FROM search_clean WHERE manufacturer = ?"
            cursor.execute(query, (manufacturer,))
            models = cursor.fetchall()
            category_data[manufacturer] = [model[0] for model in models]
        models_by_category[category] = category_data

    conn.close()
    return models_by_category


# 색상 목록 가져오기
def get_colors():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT color FROM new_info WHERE color IS NOT NULL")
    colors = cursor.fetchall()
    conn.close()
    return [color[0] for color in colors if color[0]]  # None 값 제거

# 차량 왼쪽 카테고리 모델
def get_models_by_manufacturer(manufacturer):
    # DB 연결
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 쿼리 작성: '현대' 제조사의 모델들만 가져오기
    query = "SELECT DISTINCT model FROM search_clean WHERE manufacturer = ?"
    cursor.execute(query, (manufacturer,))
    models = cursor.fetchall()

    conn.close()
    return [model[0] for model in models]  # 모델 이름 리스트 반환

def get_car_data_from_db(search_query=None, manufacturers=None, models=None,
                          min_mileage=None, max_mileage=None, min_year=None, max_year=None, color=None):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    query = "SELECT * FROM new_info WHERE 1=1"  # 기본 쿼리
    params = []

    # search_query가 있을 경우, manufacturer와 model에 대해 부분 일치 검색 수행
    if search_query:
        query += " AND (manufacturer LIKE ? OR model LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    # 색상 필터링 추가
    if color:
        placeholders = ", ".join(["?" for _ in color])
        query += f" AND color IN ({placeholders})"
        params.extend(color)
        print(f"색상 필터링 쿼리: {query}")  # 디버깅용 로그
        print(f"색상 필터링 파라미터: {params}")  # 디버깅용 로그

    # manufacturer 필터링
    if manufacturers:
        manufacturer_clauses = " OR ".join(["manufacturer LIKE ?" for _ in manufacturers])
        query += f" AND ({manufacturer_clauses})"
        params.extend([f"%{manufacturer}%" for manufacturer in manufacturers])

    # model 필터링
    if models:
        model_clauses = " OR ".join(["model LIKE ?" for _ in models])
        query += f" AND ({model_clauses})"
        params.extend([f"%{model}%" for model in models])

    # mileage 필터링
    if min_mileage:
        query += " AND mileage >= ?"
        params.append(min_mileage)
    if max_mileage:
        query += " AND mileage <= ?"
        params.append(max_mileage)

    # FormYear 필터링 (연식 기준)
    if min_year:
        query += " AND FormYear >= ?"
        params.append(min_year)
    if max_year:
        query += " AND FormYear <= ?"
        params.append(max_year)

    cur.execute(query, params)
    cars = cur.fetchall()

    car_list = []
    for car_item in cars:
        car_data = {
            "id": car_item[0],
            "manufacturer": car_item[1],
            "model": car_item[2],
            "price": f"{car_item[3]} 만원",
            "mileage": f"{car_item[4]} km",
            "year": car_item[5],  # 여기서 'FormYear' 컬럼 사용
            "fuel_type": car_item[6],
            "badge": car_item[7],
            "color": car_item[21],
            "image": f"http://ci.encar.com/carpicture{car_item[8]}001.jpg?impolicy=heightRate&rh=300&cw=400&ch=300&cg=Center&wtmk=http://ci.encar.com/wt_mark/w_mark_04.png&wtmkg=SouthEast&wtmkw=42&wtmkh=18&t=20241103163900"
        }
        car_list.append(car_data)

    conn.close()
    return car_list

# 페이지 번호 논리
def get_page_data(page, car_list):
    cars_per_page = 20
    start_index = (page - 1) * cars_per_page
    end_index = start_index + cars_per_page
    return car_list[start_index:end_index]

def get_normalized_value(table_name, original_value):
    db_path = "database.db"
    connection = sqlite3.connect(db_path)
    query = f"SELECT normalized_value FROM {table_name} WHERE original_value = ?"
    result = pd.read_sql(query, connection, params=(original_value,))

    connection.close()

    if result.empty:
        return None  # 값이 없으면 None 반환
    return result['normalized_value'].iloc[0]

def get_car_data(car_id):
    # Step 1: 데이터베이스 연결
    db_path = "database.db"
    connection = sqlite3.connect(db_path)

    # Step 2: 해당 ID의 데이터를 가져오기
    query = """
    SELECT 
        Manufacturer, Model, Price, Mileage, FormYear, FuelType, Badge, rdate,
        transmission_type, ppm, carbon, accident, transmission, 
        sylinder_cover_oil, sylinder_head_oil, sylinder_block_oil, 
        coolant_sylinder, coolant_water, coolant_radiator
    FROM new_info
    WHERE Id = ?
    """
    car_data = pd.read_sql(query, connection, params=(car_id,))

    # 데이터가 없을 경우 처리
    if car_data.empty:
        connection.close()
        return {"error": "No data found for the given ID"}

    # Step 3: 모델 이름 합치기
    fuel_Type = car_data["FuelType"]
    transmission_Type = car_data["transmission_type"]

    # Step 4: 모델 로드
    try:
        rf_model = joblib.load("random_forest_model.pkl")
    except FileNotFoundError:
        connection.close()
        return {"error": "Random forest model file not found"}


    # Step 5: 예측에 사용할 특성 선택 및 데이터 전처리
    car_data['model_Name'] = (car_data['Manufacturer'] + " " + car_data['Model']
                              + " " + car_data['Badge'])  # model_Name 생성

    features = [
        'model_Name', 'Mileage', 'FormYear', 'FuelType', 'rdate',
        'transmission_type', 'ppm', 'carbon', 'accident', 'transmission',
        'sylinder_cover_oil', 'sylinder_head_oil', 'sylinder_block_oil',
        'coolant_sylinder', 'coolant_water', 'coolant_radiator'
    ]

    # 예측용 데이터 준비
    X = car_data[features]

    # Step 5.1: FuelType 및 transmission_type 변환
    def convert_fuel_type(fuel_type):
        if fuel_type == '가솔린':
            return 0
        elif fuel_type == '디젤':
            return 1
        elif fuel_type == '가솔린+전기':
            return 2
        elif fuel_type == 'LPG(일반인 구입)':
            return 3
        else:
            return 4

    def convert_transmission_type(trans_type):
        if trans_type == '오토':
            return 1
        else:
            return 0

    def process_rdate(rdate):
        rdate = int(rdate)  # 문자열로 저장된 rdate를 정수로 변환
        rdate_year = (rdate // 10000) - 2000
        rdate_month = ((rdate % 10000) // 100) + rdate_year * 12
        processed_rdate = (rdate % 100) + rdate_month * 30
        return processed_rdate

    def process_formyear(formyear):
        form = int(formyear) - 2000
        return form

    # FuelType과 transmission_type 변환
    X = X.copy()  # X의 복사본을 만들어서 수정하는 방식으로

    # FuelType과 transmission_type 변환
    X.loc[:, 'FuelType'] = X['FuelType'].apply(convert_fuel_type)
    X.loc[:, 'transmission_type'] = X['transmission_type'].apply(convert_transmission_type)
    X.loc[:, 'rdate'] = X['rdate'].apply(process_rdate)
    X.loc[:, 'FormYear'] = X['FormYear'].apply(process_formyear)

    model_Name = car_data['model_Name'].iloc[0]
    # 정규화
    X.loc[:, 'model_Name'] = X['model_Name'].apply(lambda x: get_normalized_value('change', x))

    # Step 6: 가격 예측
    predicted_price = rf_model.predict(X)[0]

    # Step 7: 결과 생성
    car_data = car_data.iloc[0].to_dict()  # ID에 해당하는 데이터를 딕셔너리로 변환
    car_data["Predicted Price"] = round(predicted_price, 2)  # 예측된 가격 추가
    Price = car_data["Price"]
    Predicted_Price = car_data["Predicted Price"]
    Mileage = car_data["Mileage"]
    ppm = car_data['ppm']
    carbon = car_data["carbon"]
    accident = car_data["accident"]
    transmission = car_data["transmission"]
    sylinder_cover_oil = car_data["sylinder_cover_oil"]
    sylinder_head_oil = car_data["sylinder_head_oil"]
    sylinder_block_oil = car_data["sylinder_block_oil"]
    coolant_sylinder = car_data["coolant_sylinder"]
    coolant_water = car_data["coolant_water"]
    coolant_radiator = car_data["coolant_radiator"]
    match_flag = 0
    if Price >= Predicted_Price:
        match_flag = 1

    connection.close()  # 데이터베이스 연결 닫기

    # 역 정규화된 모델 이름 반환
    return (model_Name, Predicted_Price, Price, match_flag, Mileage, fuel_Type, transmission_Type, ppm, carbon,
            accident, transmission, sylinder_cover_oil, sylinder_head_oil, sylinder_block_oil, coolant_sylinder,
            coolant_water, coolant_radiator)

@app.route('/')
def car_listings():
    page = int(request.args.get('page', 1))  # 현재 페이지 번호 가져오기
    search_query = request.args.get('search', '')  # 검색어 가져오기

    # 사용자 입력 필터 가져오기
    manufacturers = request.args.getlist('manufacturer')  # 제조사 필터
    models = request.args.getlist('model')  # 모델 필터
    selected_colors = request.args.getlist('color')  # 색상 필터

    min_mileage = request.args.get('min_mileage', type=int)
    max_mileage = request.args.get('max_mileage', type=int)
    min_year = request.args.get('min_year', type=int)
    max_year = request.args.get('max_year', type=int)

    # 색상 목록 가져오기
    color = get_colors()

    # DB에서 차량 데이터 가져오기
    car_list = get_car_data_from_db(
        search_query=search_query,
        manufacturers=manufacturers,
        models=models,
        min_mileage=min_mileage,
        max_mileage=max_mileage,
        min_year=min_year,
        max_year=max_year,
        color=selected_colors  # 색상 필터 전달
    )

    # 페이지네이션 처리
    total_cars = len(car_list)
    cars_per_page = 20
    total_pages = ceil(total_cars / cars_per_page)
    current_page_cars = get_page_data(page, car_list)  # 현재 페이지 데이터만 가져오기
    page_range = range(max(1, page - 2), min(total_pages + 1, page + 3))  # 페이지 범위 설정

    return render_template(
        'search.html',
        car_list=current_page_cars,
        page=page,
        total_pages=total_pages,
        search_query=search_query,
        manufacturers=manufacturers,
        models_by_manufacturer={m: get_models_by_manufacturer(m) for m in ['현대', '기아', '쉐보레(GM대우)', '르노코리아(삼성)', '제네시스']},
        models_by_outcountry=get_models_for_outcountry(),
        selected_models=models,
        min_mileage=min_mileage,
        max_mileage=max_mileage,
        min_year=min_year,
        max_year=max_year,
        page_range=page_range,
        color=color,  # 모든 색상 전달
        selected_colors=selected_colors  # 선택된 색상 전달
    )

@app.route('/result', methods=['GET'])
async def result():
    car_id = request.args.get('car_id')  # URL에서 car_id 가져오기

    if not car_id:
        return render_template('error.html', error_message='차량 ID가 제공되지 않았습니다.')

    # 스크래핑 및 가격 계산
    try:
        # get_car_data()와 crawling()에서 데이터를 가져옵니다.
        (car_name, price, price_value, match_flag, mileage, fuel_type, transmission_type, ppm, carbon,
         accident, transmission, sylinder_cover_oil, sylinder_head_oil, sylinder_block_oil, coolant_sylinder,
         coolant_water, coolant_radiator) = get_car_data(car_id)

        (tuning, special, using, recall, hood, fh_left, fh_right, fd_left, fd_right, ld_left, ld_right, rs, fp,
         fhh_left, fhh_right, rhh_left, rhh_right) = crawling(car_id)

        # 연료 및 변속기 타입 매핑
        t_type = "수동" if transmission_type.iloc[0] == 0 else "오토"

        # 상태 매핑 함수화
        def map_status(value, mapping):
            return mapping.get(value, "알 수 없음")

        oil_status_mapping = {2: "없음", 1: "미세누유", 0: "누유"}
        coolant_status_mapping = {2: "없음", 1: "미세누수", 0: "누수"}

        transmission = "양호" if transmission == 0 else "불량"
        sylinder_cover_oil = map_status(sylinder_cover_oil, oil_status_mapping)
        sylinder_head_oil = map_status(sylinder_head_oil, oil_status_mapping)
        sylinder_block_oil = map_status(sylinder_block_oil, oil_status_mapping)
        coolant_sylinder = map_status(coolant_sylinder, coolant_status_mapping)
        coolant_water = map_status(coolant_water, coolant_status_mapping)
        coolant_radiator = map_status(coolant_radiator, coolant_status_mapping)

        # 튜닝, 특별 이력 등 상태 매핑
        tuning = "없음" if tuning else "있음"
        special = "없음" if special else "있음"
        using = "없음" if using else "있음"
        recall = "없음" if recall else "있음"

        # 사고 이력 생성
        damage_report_parts = []
        part_labels = {
            "후드": hood,
            "프론트 휀더(좌)": fh_left,
            "프론트 휀더(우)": fh_right,
            "프론트 도어(좌)": fd_left,
            "프론트 도어(우)": fd_right,
            "리어 도어(좌)": ld_left,
            "리어 도어(우)": ld_right,
            "라디에이터 서포트(볼트체결부품)": rs,
            "프론트 패널": fp,
            "프론트 휠하우스(좌)": fhh_left,
            "프론트 휠하우스(우)": fhh_right,
            "리어 휠하우스(좌)": rhh_left,
            "리어 휠하우스(우)": rhh_right
        }

        for part, status in part_labels.items():
            if status == 0:
                damage_report_parts.append(part)

        report = "없음" if not damage_report_parts else ", ".join(damage_report_parts)

        # GPT에 전달할 프롬프트 생성
        prompt = (
            f"다음은 차량 평가에 대한 설명입니다.\n"
            f"차량 이름 : {car_name}\n"
            f"주행 거리 : {mileage}km\n"
            f"판매 가격 : {price}만원\n"
            f"예측한 적정 가격 : {price_value}만원\n"
            f"연료 타입 : {fuel_type.iloc[0]}\n"
            f"변속기 종류 : {t_type}\n"
            f"배출가스 : {ppm}\n"
            f"탄화가스 : {carbon}\n"
            f"변속기 상태 : {transmission}\n"
            f"실린더 커버 오일 누유 : {sylinder_cover_oil}\n"
            f"실린더 헤드 오일 누유 : {sylinder_head_oil}\n"
            f"실린더 블록 오일 누유 : {sylinder_block_oil}\n"
            f"냉각수 실린더 누수 : {coolant_sylinder}\n"
            f"냉각수 워터펌프 누수 : {coolant_water}\n"
            f"냉각수 라디에이터 누수 : {coolant_radiator}\n"
            f"튜닝 이력 : {tuning}\n"
            f"특별 이력 : {special}\n"
            f"용도 변경 : {using}\n"
            f"리콜 여부 : {recall}\n"
            f"사고 이력 : {report}"
            f"이 차량의 장단점과 구매 추천 여부를 간단하게 평가해주세요."
        )

        prompt = f'<p>{prompt}<p>'
        # GPT-4 응답 생성
        text = await answer(prompt)

        return render_template('result.html',
                               name=car_name,
                               price=round(price, 3),
                               real_price=price_value,
                               match_flag=match_flag,
                               mileage=mileage,
                               fuel_type=fuel_type.iloc[0],
                               transmission=t_type,
                               text=text)

    except Exception as e:
        return render_template('error.html', error_message=f'오류가 발생했습니다: {str(e)}')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)