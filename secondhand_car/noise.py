#노이즈 추가로 증강
import sqlite3

# 데이터베이스 연결
db_path = "database.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Step 1: all_data 테이블 생성 (데이터 증강된 결과 저장)
cursor.execute("""
CREATE TABLE IF NOT EXISTS all_data (
    model_Name INTEGER,
    Price INTEGER,
    Mileage INTEGER,
    FormYear INTEGER,
    FuelType INTEGER,
    rdate REAL,
    transmission_type REAL,
    ppm REAL,
    carbon REAL,
    accident REAL,
    transmission REAL,
    sylinder_cover_oil REAL,
    sylinder_head_oil REAL,
    sylinder_block_oil REAL,
    coolant_sylinder REAL,
    coolant_water REAL,
    coolant_radiator REAL
)
""")

# Step 2: 데이터 추출 (use_data 테이블에서)
cursor.execute("SELECT * FROM use_data")
columns = [description[0] for description in cursor.description]

# 데이터를 가져와서 조건에 맞춰 변형
for row in cursor.fetchall():
    data = dict(zip(columns, row))

    # 1번: Mileage 5% 증가, Price 1% 증가
    data1 = data.copy()
    data1['Mileage'] = int(data['Mileage'] * 1.05)
    data1['Price'] = int(data['Price'] * 1.01)

    # 2번: Mileage 5% 감소, Price 1% 감소
    data2 = data.copy()
    data2['Mileage'] = int(data['Mileage'] * 0.95)
    data2['Price'] = int(data['Price'] * 0.99)

    # 3번: FormYear 360 감소, Price 1% 감소
    data3 = data.copy()
    data3['FormYear'] = data['FormYear'] - 360
    data3['Price'] = int(data['Price'] * 0.99)

    # 4번: FormYear 360 증가, Price 1% 증가
    data4 = data.copy()
    data4['FormYear'] = data['FormYear'] + 360
    data4['Price'] = int(data['Price'] * 1.01)

    # 5번: ppm 20% 증가, Price는 그대로
    data5 = data.copy()
    data5['ppm'] = int(data['ppm'] * 1.2)

    # 6번: ppm 20% 감소, Price는 그대로
    data6 = data.copy()
    data6['ppm'] = int(data['ppm'] * 0.8)

    # 7번: carbon 10% 증가, Price는 그대로
    data7 = data.copy()
    data7['carbon'] = int(data['carbon'] * 1.1)

    # 8번: carbon 10% 감소, Price는 그대로
    data8 = data.copy()
    data8['carbon'] = int(data['carbon'] * 0.9)

    # 9번: 1번과 3번 조건 동시에
    data9 = data.copy()
    data9['Mileage'] = int(data['Mileage'] * 1.05)
    data9['Price'] = int(data['Price'] * 1.01)
    data9['FormYear'] = data['FormYear'] - 360

    # 10번: 2번과 4번 조건 동시에
    data10 = data.copy()
    data10['Mileage'] = int(data['Mileage'] * 0.95)
    data10['Price'] = int(data['Price'] * 0.99)
    data10['FormYear'] = data['FormYear'] + 360

    # 11번: 1번 조건을 2배로
    data11 = data.copy()
    data11['Mileage'] = int(data['Mileage'] * 1.10)  # 5% 증가를 2배로, 10% 증가
    data11['Price'] = int(data['Price'] * 1.02)  # 1% 증가를 2배로, 2% 증가

    # 12번: 2번 조건을 2배로
    data12 = data.copy()
    data12['Mileage'] = int(data['Mileage'] * 0.90)  # 5% 감소를 2배로, 10% 감소
    data12['Price'] = int(data['Price'] * 0.98)  # 1% 감소를 2배로, 2% 감소

    # 13번: 3번 조건을 2배로
    data13 = data.copy()
    data13['FormYear'] = data['FormYear'] - 720  # 360 감소를 2배로, 720 감소
    data13['Price'] = int(data['Price'] * 0.98)  # 1% 감소를 2배로, 2% 감소

    # 14번: 4번 조건을 2배로
    data14 = data.copy()
    data14['FormYear'] = data['FormYear'] + 720  # 360 증가를 2배로, 720 증가
    data14['Price'] = int(data['Price'] * 1.02)  # 1% 증가를 2배로, 2% 증가

    # 증강된 데이터를 all_data 테이블에 삽입
    for augmented_data in [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12,
                           data13, data14]:
        cursor.execute("""
        INSERT INTO all_data (
            model_Name, Price, Mileage, FormYear, FuelType, rdate,
            transmission_type, ppm, carbon, accident, transmission,
            sylinder_cover_oil, sylinder_head_oil, sylinder_block_oil,
            coolant_sylinder, coolant_water, coolant_radiator
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            augmented_data['model_Name'],
            augmented_data['Price'],
            augmented_data['Mileage'],
            augmented_data['FormYear'],
            augmented_data['FuelType'],
            augmented_data['rdate'],
            augmented_data['transmission_type'],
            augmented_data['ppm'],
            augmented_data['carbon'],
            augmented_data['accident'],
            augmented_data['transmission'],
            augmented_data['sylinder_cover_oil'],
            augmented_data['sylinder_head_oil'],
            augmented_data['sylinder_block_oil'],
            augmented_data['coolant_sylinder'],
            augmented_data['coolant_water'],
            augmented_data['coolant_radiator']
        ))

# 데이터베이스 커밋 및 종료
connection.commit()

# 데이터베이스 연결 닫기
connection.close()
