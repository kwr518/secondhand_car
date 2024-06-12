import numpy as np
import pandas as pd
import sqlite3
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LeakyReLU, Input
from tensorflow.keras.optimizers import Adam


# 데이터베이스에서 데이터 로드
def load_data():
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM use_data"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# 데이터베이스에 저장
def save_data_to_db(data, table_name="gan_data"):
    conn = sqlite3.connect("database.db")
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"{table_name} 테이블에 데이터가 저장되었습니다.")


# 데이터 전처리
def preprocess_data(df):
    fixed_columns = [
        "model_Name", "FuelType", "transmission_type", "accident",
        "transmission", "sylinder_cover_oil", "sylinder_head_oil",
        "sylinder_block_oil", "coolant_sylinder", "coolant_water", "coolant_radiator"
    ]
    fixed_data = df[fixed_columns]
    target_columns = list(set(df.columns) - set(fixed_columns))
    target_data = df[target_columns]

    # 정규화 (0~1)
    target_data = (target_data - target_data.min()) / (target_data.max() - target_data.min())
    return fixed_data, target_data, target_columns


# 역정규화
def inverse_transform(data, original_df, target_columns):
    for col in target_columns:
        data[col] = data[col] * (original_df[col].max() - original_df[col].min()) + original_df[col].min()
    return data


# GAN 모델 설계
def build_gan(input_dim):
    # 생성자
    generator = Sequential([
        Input(shape=(input_dim,)),
        Dense(128),
        LeakyReLU(0.2),
        Dense(256),
        LeakyReLU(0.2),
        Dense(input_dim, activation='sigmoid')
    ])

    # 판별자
    discriminator = Sequential([
        Input(shape=(input_dim,)),
        Dense(256),
        LeakyReLU(0.2),
        Dense(128),
        LeakyReLU(0.2),
        Dense(1, activation='sigmoid')
    ])
    discriminator.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

    # GAN 모델
    discriminator.trainable = False
    gan_input = Input(shape=(input_dim,))
    generated_data = generator(gan_input)
    gan_output = discriminator(generated_data)
    gan = Model(gan_input, gan_output)
    gan.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

    return generator, discriminator, gan


def train_gan(generator, discriminator, gan, data, epochs=5000, batch_size=32):
    for epoch in range(epochs):
        try:
            # 실제 데이터 샘플링
            real_data = data.sample(batch_size, replace=True).values  # NumPy 배열로 변환
            real_labels = np.ones((batch_size, 1))  # 실제 데이터 라벨

            # 가짜 데이터 생성
            noise = np.random.normal(0, 1, (batch_size, data.shape[1]))
            fake_data = generator.predict(noise)
            fake_labels = np.zeros((batch_size, 1))  # 가짜 데이터 라벨
#1
            # 판별자 학습
            discriminator.trainable = True
            d_loss_real = discriminator.train_on_batch(real_data, real_labels)
            d_loss_fake = discriminator.train_on_batch(fake_data, fake_labels)
            d_loss = 0.5 * (d_loss_real + d_loss_fake)  # 단순 평균

            # 생성자 학습
            discriminator.trainable = False
            noise = np.random.normal(0, 1, (batch_size, data.shape[1]))
            valid_labels = np.ones((batch_size, 1))  # 생성자 학습 라벨은 '진짜'로 설정
            g_loss = gan.train_on_batch(noise, valid_labels)

            # 진행 상황 출력
            if epoch % 100 == 0:
                print(f"Epoch {epoch} | D Loss: {d_loss:.4f} | G Loss: {g_loss:.4f}")

        except Exception as e:
            print(f"error {epoch}에서 오류 발생: {e}")



# 메인 실행
def main():
    # 데이터 로드
    df = load_data()

    # 데이터 전처리
    fixed_data, target_data, target_columns = preprocess_data(df)

    # GAN 모델 생성
    input_dim = target_data.shape[1]
    generator, discriminator, gan = build_gan(input_dim)

    # GAN 학습
    train_gan(generator, discriminator, gan, target_data)

    # 새로운 데이터 생성
    num_samples = 1000000
    noise = np.random.normal(0, 1, (num_samples, input_dim))
    generated_data = generator.predict(noise)

    # 데이터 역정규화 및 결합
    generated_data = pd.DataFrame(generated_data, columns=target_columns)
    generated_data = inverse_transform(generated_data, df, target_columns)
    final_data = pd.concat([fixed_data.sample(num_samples, replace=True).reset_index(drop=True), generated_data], axis=1)

    # 데이터 저장
    save_data_to_db(final_data)


if __name__ == "__main__":
    main()
