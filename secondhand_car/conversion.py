import sqlite3

# 데이터베이스 연결
db_path = "database.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Step 1: change 테이블 생성 및 Name 정규화
cursor.execute("""
CREATE TABLE IF NOT EXISTS change (
    original_value TEXT UNIQUE,
    normalized_value INTEGER PRIMARY KEY AUTOINCREMENT
)
""")

# Manufacturer, Model, Badge를 결합하여 Name으로 정규화하고 change 테이블에 저장
def normalize_column_for_name():
    cursor.execute("SELECT DISTINCT Manufacturer, Model, Badge FROM new_info")
    unique_values = cursor.fetchall()

    for value in unique_values:
        combined_value = f"{value[0]} {value[1]} {value[2]}"  # Manufacturer, Model, Badge를 결합
        cursor.execute("""
        INSERT OR IGNORE INTO change (original_value) VALUES (?)
        """, (combined_value,))
    connection.commit()

normalize_column_for_name()  # Name 정규화

# Step 2: use_data 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS use_data (
    model_Name INTEGER,
    Price REAL,
    Mileage INTEGER,
    FormYear INTEGER,
    FuelType INTEGER,
    rdate REAL,
    transmission_type INTEGER,
    ppm INTEGER,
    carbon REAL,
    accident INTEGER,  
    transmission INTEGER,
    sylinder_cover_oil INTEGER,
    sylinder_head_oil INTEGER,
    sylinder_block_oil INTEGER,
    coolant_sylinder INTEGER,
    coolant_water INTEGER,
    coolant_radiator INTEGER
)
""")

# Step 3: 데이터 변환 및 저장
def convert_fuel_type(fuel_type):
    mapping = {
        '가솔린': 0,
        '디젤': 1,
        '가솔린+전기': 2,
        'LPG(일반인 구입)': 3
    }
    return mapping.get(fuel_type, 4)

def convert_transmission_type(transmission_type):
    return 1 if transmission_type == '오토' else 0

# 데이터 변환 및 use_data로 저장
cursor.execute("SELECT * FROM new_info")
columns = [description[0] for description in cursor.description]

for row in cursor.fetchall():
    data = dict(zip(columns, row))

    # 결측치가 있는지 확인하고, 있으면 해당 데이터를 건너뜁니다
    if any(value is None for value in data.values()):
        continue  # 결측치가 있으면 해당 데이터를 건너뛰고, 다음 데이터로 넘어감

    # Manufacturer, Model, Badge를 결합하여 Name을 정규화
    combined_name = f"{data['Manufacturer']} {data['Model']} {data['Badge']}"
    cursor.execute("SELECT normalized_value FROM change WHERE original_value = ?", (combined_name,))
    name_normalized = cursor.fetchone()[0]

    # FuelType 변환
    fuel_type_transformed = convert_fuel_type(data['FuelType'])

    # transmission_type 변환
    transmission_type_transformed = convert_transmission_type(data['transmission_type'])

    # FormYear에서 2000 빼기
    form_year_transformed = data['FormYear'] - 2000

    # rdate 단위 변경
    rdate_year = (int(data['rdate']) / 10000) - 2000
    rdate_month = (int(data['rdate'] % 10000) / 100) + rdate_year * 12
    rdate_transformed = (data['rdate'] % 100) + rdate_month * 30

    # Price 값이 None이거나 9999 이상인 경우, 데이터를 삽입하지 않음
    if data['Price'] is None or data['Price'] >= 9999:
        continue  # 해당 데이터를 건너뛰고, 다음 데이터로 넘어감

    # use_data에 삽입
    cursor.execute("""
    INSERT INTO use_data (
        model_Name, Price, Mileage, FormYear, FuelType, rdate,
        transmission_type, ppm, carbon, accident, transmission,
        sylinder_cover_oil, sylinder_head_oil, sylinder_block_oil,
        coolant_sylinder, coolant_water, coolant_radiator
    )
    VALUES (?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?)
    """, (
        name_normalized,  # Name 정규화된 값으로 저장
        data['Price'],
        data['Mileage'],
        form_year_transformed,  # FormYear에서 2000을 뺀 값 저장
        fuel_type_transformed,
        rdate_transformed,  # rdate에서 20000000을 뺀 값 저장
        transmission_type_transformed,
        data['ppm'],
        data['carbon'],
        data['accident'],
        data['transmission'],
        data['sylinder_cover_oil'],
        data['sylinder_head_oil'],
        data['sylinder_block_oil'],
        data['coolant_sylinder'],
        data['coolant_water'],
        data['coolant_radiator']
    ))

connection.commit()

# Step 4: 역변환 함수
def denormalize_value(normalized_value):
    cursor.execute("SELECT original_value FROM change WHERE normalized_value = ?", (normalized_value,))
    return cursor.fetchone()[0]

# 역변환 테스트
normalized_example = 1  # 예: 정규화된 Name의 값
original_value = denormalize_value(normalized_example)
print(f"Normalized: {normalized_example} -> Original: {original_value}")

# 데이터베이스 연결 닫기
connection.close()
