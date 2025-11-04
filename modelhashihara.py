import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime
import os
import joblib

# ==========================================================
# KONSTANTA & MAPPING
# ==========================================================
FILE_DATA = "data.csv"
FILE_PREDIKSI = "hasil_prediksi.csv"
FILE_MODEL = "color_vision_model.pkl" # Nama file model yang disimpan
FILE_LE = "label_encoder_rf.pkl"         # Simpan LabelEncoder (jika diperlukan, meski RF bisa string)

# Definisikan Mapping Feedback dan Keterangan (Menggantikan if-else)
FEEDBACK_MAPPING = {
    "buta warna total": {
        "keterangan": "buta warna total",
        "feedback": (
            "Hasil tes menunjukkan bahwa Anda mengalami kesulitan dalam membedakan warna. "
            "Kami menyarankan agar Anda berkonsultasi dengan dokter spesialis mata untuk pemeriksaan lebih lanjut. "
            "Tes lebih lanjut dapat membantu mendapatkan diagnosis yang lebih akurat."
        )
    },
    "buta warna parsial": {
        "keterangan": "buta warna parsial",
        "feedback": (
            "Hasil tes menunjukkan bahwa Anda memiliki kemampuan penglihatan warna yang cukup baik. "
            "Namun, mungkin ada beberapa kondisi atau warna yang masih cukup menantang untuk Anda. "
            "Kami sarankan untuk terus berlatih dan tetap menjaga kesehatan mata."
        )
    },
    "normal": {
        "keterangan": "normal",
        "feedback": (
            "Hasil tes menunjukkan bahwa kemampuan penglihatan warna Anda sangat baik. "
            "Anda dapat membedakan warna dengan jelas dan tajam dalam berbagai kondisi. "
            "Terus pertahankan penglihatan Anda dengan menjaga kesehatan mata secara rutin!"
        )
    }
}

# ==========================================================
# FUNGSI UTAMA
# ==========================================================

def train_and_generate_feedback():
    """Melatih model Random Forest, menghitung akurasi, menyimpan model, dan membuat hasil_prediksi.csv."""
    
    # --- 1. Load data.csv ---
    if not os.path.exists(FILE_DATA):
        print(f"Error: File '{FILE_DATA}' tidak ditemukan. Harap jalankan aplikasi utama untuk membuat data terlebih dahulu.")
        return

    data = pd.read_csv(FILE_DATA)

    # Menghilangkan data kotor/inkonsisten (Cleaning)
    def clean_label(keterangan):
        return FEEDBACK_MAPPING[keterangan]['keterangan'] if keterangan in FEEDBACK_MAPPING else "normal"

    # Pastikan label bersih dan sesuai kunci mapping
    data["label"] = data["keterangan"].apply(clean_label)
    
    # --- 2. Persiapan dan Pelatihan ---
    X = data[["skor"]]
    y = data["label"]
    skip_accuracy = False
    
    if len(data) < 2:
        print("Jumlah data kurang dari 2. Model tetap dilatih, namun akurasi tidak dihitung.")
        X_train = X
        y_train = y
        X_test = X
        y_test = y
        skip_accuracy = True
    else:
        # Pisahkan Data Uji dan Latih
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
    print("Memulai pelatihan model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # --- 3. Simpan Model dan Akurasi ---
    joblib.dump(model, FILE_MODEL)
    print(f"Model berhasil disimpan ke {FILE_MODEL}")

    if not skip_accuracy:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred) * 100
        print(f"Akurasi Model pada data uji: {accuracy:.2f}%")

    # --- 4. Prediksi dan Mapping Feedback (Vektorisasi & Tanpa if-else) ---
    
    # Vektorisasi: Prediksi untuk seluruh dataset (termasuk data user terbaru)
    data["prediksi"] = model.predict(data[["skor"]])
    
    # Mapping Data (Menggunakan dictionary mapping)
    data["feedback_data"] = data["prediksi"].apply(lambda p: FEEDBACK_MAPPING.get(p))
    
    # Ekstraksi Keterangan dan Feedback dari kolom dictionary baru
    data["keterangan_prediksi"] = data["feedback_data"].apply(lambda d: d["keterangan"])
    data["feedback"] = data["feedback_data"].apply(lambda d: d["feedback"])
    
    # --- 5. Simpan Hasil ---
    
    hasil = pd.DataFrame({
        "skor": data["skor"],
        "keterangan": data["keterangan_prediksi"],
        "feedback": data["feedback"],
        "waktu_userinp": data.get("waktu", "Tidak Tersedia"),
        "waktu_akurasi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    # Simpan hasil prediksi
    hasil.to_csv(FILE_PREDIKSI, index=False)
    print(f"Prediksi berhasil disimpan ke {FILE_PREDIKSI}")

if __name__ == "__main__":
    train_and_generate_feedback()