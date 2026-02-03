import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

def train_and_save_model():
    # Pastikan file data.csv ada
    if not os.path.exists('data.csv'):
        print("data.csv tidak ditemukan. Buat beberapa entri data secara manual atau jalankan aplikasi dulu.")
        print("Membuat contoh data dummy...")
        data = {
            'skor': [5, 12, 23, 8, 18, 24],
            'keterangan': ['buta warna total', 'buta warna parsial', 'normal', 'buta warna total', 'buta warna parsial', 'normal']
        }
        df = pd.DataFrame(data)
        df.to_csv('data.csv', index=False)
        print("Contoh data.csv berhasil dibuat.")

    # Muat data
    df = pd.read_csv('data.csv')

    # Siapkan data untuk model
    X = df[['skor']]  # Fitur: skor
    y = df['keterangan'] # Target: keterangan

    # Latih model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # Simpan model
    joblib.dump(model, 'color_vision_model.pkl')
    print("Model 'color_vision_model.pkl' berhasil dilatih dan disimpan.")

if __name__ == '__main__':
    train_and_save_model()