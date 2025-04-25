import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime
import os

# --- Load data.csv ---
data = pd.read_csv("data.csv")

if len(data) >= 20:
    # Label berdasarkan skor
    def get_label(skor):
        if skor <= 2:
            return "Kurang Menguasai"
        elif skor == 3:
            return "Menguasai"
        else:
            return "Sangat Menguasai"

    data["label"] = data["skor"].apply(get_label)

    # Split & train
    X = data[["skor"]]  # Fitur (skor)
    y = data["label"]   # Label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Membuat model dan melatihnya
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Menghitung akurasi berdasarkan X_test dan y_test
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100  # Akurasi dalam persen

    # Simpan hasil prediksi untuk seluruh data
    results = []
    for index, row in data.iterrows():
        skor_user = row["skor"]
        
        # Membuat DataFrame untuk prediksi yang konsisten dengan data pelatihan
        X_new = pd.DataFrame([[skor_user]], columns=["skor"])  # Kolom "skor" harus sama
        prediksi = model.predict(X_new)[0]  # Prediksi berdasarkan skor
        
        # Menyimpan waktu prediksi
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Menambahkan hasil ke dalam list
        results.append({
            "skor": skor_user,
            "keterangan": prediksi,
            "waktu": waktu,
            "akurasi": f"{accuracy:.2f}%"  # Akurasi ditambahkan sekali saja
        })

    # Simpan ke hasil_prediksi.csv
    hasil = pd.DataFrame(results)

    # Cek apakah hasil_prediksi.csv sudah ada
    file_exists = os.path.exists("hasil_prediksi.csv")

    # Append data ke hasil_prediksi.csv dengan header jika file baru
    hasil.to_csv("hasil_prediksi.csv", index=False, mode='w', header=not file_exists)

    print("Prediksi dan akurasi berhasil disimpan ke hasil_prediksi.csv")

else:
    print("Belum cukup data untuk pengujian. Minimal 20 data di data.csv.")
