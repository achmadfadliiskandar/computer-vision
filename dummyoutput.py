import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC # Support Vector Classifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os
import random
import datetime

# ==========================================================
# KONSTANTA DAN FILE PATH
# ==========================================================
FILE_DATA = "data.csv"
FILE_MODEL = "color_vision_model.pkl"
FILE_LE = "label_encoder.pkl" 
DATA_SAMPLES_TO_ADD = 2000 # Jumlah data dummy yang akan ditambahkan setiap kali pelatihan

# ==========================================================
# FUNGSI GENERASI DATA DUMMY (Sekarang Selalu Menambahkan)
# ==========================================================
def add_dummy_data(n_samples):
    """Menghasilkan data dummy buta warna dan menambahkannya ke FILE_DATA."""
    
    # Cek apakah file sudah ada untuk menentukan apakah header perlu ditulis
    file_exists = os.path.exists(FILE_DATA)
    
    dummy_data = []
    for _ in range(n_samples):
        skor = random.randint(1, 24)
        if skor <= 9:
            keterangan = "buta warna total"
        elif 10 <= skor <= 21:
            keterangan = "buta warna parsial"
        else: # 22 <= skor <= 24
            keterangan = "normal"
        dummy_data.append({"skor": skor, "keterangan": keterangan, "waktu": datetime.datetime.now().strftime("%X")})
    
    df_dummy = pd.DataFrame(dummy_data)
    
    # Menggunakan mode='a' (append) dan header=not file_exists
    df_dummy.to_csv(FILE_DATA, index=False, mode='a', header=not file_exists)
    print(f"✅ {n_samples} data dummy baru berhasil ditambahkan ke {FILE_DATA}.")

# ==========================================================
# PROSES PELATIHAN DAN PENGUJIAN AKURASI
# ==========================================================
def train_and_save_model():
    """Menambahkan data, melatih model, mengukur akurasi, dan menyimpannya."""
    print("--- Memulai Pelatihan Model Buta Warna ---")
    
    # LANGKAH BARU: Selalu tambahkan data dummy sebelum membaca data
    add_dummy_data(DATA_SAMPLES_TO_ADD)

    try:
        # Baca seluruh data yang sudah diperbarui
        df = pd.read_csv(FILE_DATA)
        df = df.dropna(subset=['keterangan']) 
        
        if df.empty or 'skor' not in df.columns or 'keterangan' not in df.columns:
            print("❌ Data tidak valid. Tidak dapat melatih model.")
            return

        print(f"Total data yang digunakan untuk pelatihan: {len(df)} baris.")

        # Encoding Label
        le = LabelEncoder()
        df['keterangan_encoded'] = le.fit_transform(df['keterangan'])
        joblib.dump(le, FILE_LE)
        print(f"✅ Label Encoder berhasil disimpan ke {FILE_LE}")

        # Persiapan Data (Train-Test Split)
        X = df[['skor']] 
        y = df['keterangan_encoded'] 

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"Data latih: {len(X_train)}, Data uji: {len(X_test)}.")

        # Pelatihan Model 
        print("⏳ Mulai melatih model (SVC)...")
        model = SVC(kernel='rbf', C=0.8, random_state=42) 
        model.fit(X_train, y_train)
        print("✅ Pelatihan Selesai!")

        # Evaluasi Akurasi (pada data uji)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n==================================================")
        print(f"📈 AKURASI MODEL PADA DATA UJI: {accuracy:.4f}")
        print(f"==================================================")

        # Simpan Model
        joblib.dump(model, FILE_MODEL)
        print(f"💾 Model berhasil disimpan sebagai {FILE_MODEL}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat melatih model: {e}")

if __name__ == "__main__":
    train_and_save_model()