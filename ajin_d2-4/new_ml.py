import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# 데이터베이스 연결
db_path = "database.db"
connection = sqlite3.connect(db_path)

# Step 1: all_data 테이블에서 데이터 추출
query = """
SELECT 
    model_Name, Price, Mileage, FormYear, FuelType, rdate,
    transmission_type, ppm, carbon, accident, transmission,
    sylinder_cover_oil, sylinder_head_oil, sylinder_block_oil,
    coolant_sylinder, coolant_water, coolant_radiator
FROM all_data
"""
df = pd.read_sql(query, connection)

# Step 2: 특성과 타겟 분리
X = df.drop(columns=['Price'])  # 'Price'를 제외한 모든 변수들
y = df['Price']  # 예측하고자 하는 목표 변수는 'Price'

# Step 3: 데이터 나누기 (훈련 세트와 테스트 세트)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: 랜덤 포레스트 회귀 모델 학습
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Step 5: 예측
y_pred = rf_model.predict(X_test)

# Step 6: 모델 평가 (평균 제곱 오차)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Step 7: 테스트 데이터 예시와 예측 결과 출력
test_data_example = X_test.iloc[:5]  # 테스트 데이터에서 첫 5개 샘플을 가져옴
predictions = y_pred[:5]  # 첫 5개 예측 결과

# 테스트 데이터 예시를 딕셔너리 형태로 변환 (1차원으로 만듦)
test_data_example_flattened = test_data_example.to_dict(orient='records')

print("\nTest Data Example with Actual and Predicted Prices:")
for i in range(5):
    print(f"Example {i+1}:")
    print(f"Actual Price: {y_test.iloc[i]}")
    print(f"Predicted Price: {predictions[i]}")
    print(f"Test Data: {test_data_example_flattened[i]}\n")

# Step 8: 학습된 랜덤 포레스트 모델을 파일로 저장
joblib.dump(rf_model, 'random_forest_model.pkl')

# 데이터베이스 연결 종료
connection.close()
