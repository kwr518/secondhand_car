# 🚗 차찾자 (ChaChaJa) - AI 기반 중고차 적정 가격 예측 및 추천 서비스

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Random_Forest-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT_4o-412991?style=flat&logo=openai&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Web_Crawling-43B02A?style=flat&logo=selenium&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)

## 📖 Project Overview
**'차찾자'**는 중고차 시장의 고질적인 문제인 **정보 비대칭성**을 해결하기 위해 개발된 서비스입니다.

중고차 구매 경험이 부족한 사용자는 복잡한 성능 기록부와 차량 상태를 보고 합리적인 가격인지 판단하기 어렵습니다. 본 프로젝트는 **머신러닝(Random Forest)을 통해 적정 중고차 가격을 예측**하고, **생성형 AI(GPT-4o)를 활용해 복잡한 차량 정보를 알기 쉽게 요약**해줌으로써 사용자의 합리적인 구매 결정을 돕습니다.

---

## ✨ Key Features

### 1. 💰 AI 중고차 가격 예측
- 차량의 제원(연식, 주행거리, 연료 등)과 성능 기록부 데이터를 분석하여 **적정 시세**를 예측합니다.
- 사용자가 보고 있는 매물이 예측 가격보다 비싼지 저렴한지 직관적으로 알려줍니다.

### 2. 🤖 AI 딜러 총평 (GPT-4o)
- 복잡한 성능 기록부와 차량 상태 데이터를 **OpenAI GPT-4o** 모델에 입력하여, 마치 전문가가 조언하듯 **차량의 장단점과 구매 추천 여부**를 요약해줍니다.

### 3. 🔍 맞춤형 검색 및 필터
- 제조사, 모델, 연식, 주행거리 등 다양한 조건으로 차량을 검색하고 찜 목록(Wishlist)으로 관리할 수 있습니다.

### 4. 🕸️ 데이터 자동 수집 파이프라인
- **Encar API**와 **Web Crawling(Selenium)**을 결합하여 차량 기본 정보와 상세 성능 기록부를 자동으로 수집하고 DB화합니다.

---

## 🛠️ System Architecture

| 구성 요소 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **Data Collection** | Python, Selenium, BeautifulSoup | Encar API 및 성능기록부 크롤링 |
| **Database** | SQLite | 수집된 데이터의 중복 제거 및 구조화 저장 |
| **AI Model** | Scikit-learn (Random Forest) | 가격 예측 회귀 모델 학습 (Trees: 100, Depth: 62) |
| **Generative AI** | OpenAI API (GPT-4o) | 차량 상태 요약 및 자연어 리포트 생성 |
| **Web Frontend** | HTML, CSS, JavaScript | 사용자 인터페이스 및 시각화 |

---

## 📊 Data & Modeling (Core Tech)

### 1. 데이터 수집 및 전처리
- **Source:** 엔카(Encar) API 및 웹 사이트
- **Features:** 제조사, 모델명, 주행거리, 연식, 배기량, 사고 이력, 침수 여부 등 23가지 항목

### 2. 데이터 증강 (Data Augmentation)
모델의 일반화 성능을 높이기 위해 원본 데이터에 노이즈를 추가하는 방식으로 데이터를 5배 증강하였습니다.
- **Before:** 208,844개
- **After:** 1,253,064개

### 3. 모델 성능 개선 결과
데이터 증강 전후의 **MSE(Mean Squared Error)** 비교 결과, 오차율이 획기적으로 감소하였습니다.
- **증강 전 MSE:** 485,596
- **증강 후 MSE:** **39,049** (약 12배 성능 향상 📉)

### 4. 모델 선정 이유
- **선형 회귀(Linear Regression)**보다 비선형적인 패턴 학습에 유리하고, **SVM**보다 대용량 데이터 처리에 적합한 **Random Forest** 알고리즘을 채택하였습니다.
- 학습/검증 비율은 8:2로 설정하여 검증하였습니다.

---

## 📂 Directory Structure (Inferred)
📦 secondhand_car 
<br/>├── 📂 static # CSS, JS, 이미지 등 정적 파일 
<br/>├── 📂 templates # 웹 페이지 HTML 템플릿 
<br/>├── 📄 main.py # 웹 애플리케이션 실행 메인 파일 (Flask App) 
<br/>├── 📄 new_ml.py # Random Forest 모델 학습 및 1차 튜닝 코드 
<br/>├── 📄 new_ml2.py # 모델 성능 개선 및 재학습 코드 
<br/>├── 📄 noise.py # 데이터 증강(Data Augmentation) 로직 (노이즈 주입) 
<br/>├── 📄 gan.py # (실험적) GAN 기반 데이터 생성 스크립트 
<br/>├── 📄 conversion.py # 데이터 전처리 및 형식 변환 유틸리티 
<br/>└── 📄 .gitignore # Git 제외 파일 목록

---

## 📸 Screenshots

| 메인 화면 & 검색 | AI 예측 결과 & 딜러 총평 |
| :---: | :---: |
| ![Main Screen](https://github.com/user-attachments/assets/b03517e2-ae03-41eb-b182-e943535bc10e) | ![AI Result](https://github.com/user-attachments/assets/dbe9d375-9959-4d3c-88ab-667aeab6b16c) |
| *다양한 조건으로 차량 검색* | *적정 시세 분석 및 GPT-4o 요약* |
*(위 이미지 영역에 실제 구현 화면 캡처를 넣어주세요)*

---

## 📝 Future Work
- **데이터 파이프라인 자동화:** 주 1회 수동 업데이트 방식을 스케줄링을 통한 실시간 데이터 수집 시스템으로 개선
- **속도 최적화:** GPT-4o 생성 속도 및 추론 시간을 단축하기 위해 예측 결과 캐싱(Caching) 도입
- **개인화 추천:** 사용자 행동 로그를 기반으로 한 정교한 추천 알고리즘 적용

---

## 📜 License
This project is for educational purposes.
