import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime
import os

# --- Load data.csv ---
data = pd.read_csv("data.csv")

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

# Tampilkan akurasi di print
print(f"Akurasi Model: {accuracy:.2f}%")

# Simpan hasil prediksi untuk seluruh data tanpa akurasi
results = []
for index, row in data.iterrows():
    skor_user = row["skor"]
    
    # Membuat DataFrame untuk prediksi yang konsisten dengan data pelatihan
    X_new = pd.DataFrame([[skor_user]], columns=["skor"])  # Kolom "skor" harus sama
    prediksi = model.predict(X_new)[0]  # Prediksi berdasarkan skor
    
    # Menentukan feedback berdasarkan skor
    if skor_user <= 2:
        feedback = (
            "Hasil tes menunjukkan bahwa Anda mengalami kesulitan dalam membedakan warna. "
            "Kami menyarankan agar Anda berkonsultasi dengan dokter spesialis mata untuk pemeriksaan lebih lanjut. "
            "Tes lebih lanjut dapat membantu mendapatkan diagnosis yang lebih akurat."
        )
        keterangan = "Kurang Memuaskan"
    elif skor_user == 3:
        feedback = (
            "Hasil tes menunjukkan bahwa Anda memiliki kemampuan penglihatan warna yang cukup baik. "
            "Namun, mungkin ada beberapa kondisi atau warna yang masih cukup menantang untuk Anda. "
            "Kami sarankan untuk terus berlatih dan tetap menjaga kesehatan mata."
        )
        keterangan = "Memuaskan"
    else:
        feedback = (
            "Hasil tes menunjukkan bahwa kemampuan penglihatan warna Anda sangat baik. "
            "Anda dapat membedakan warna dengan jelas dan tajam dalam berbagai kondisi. "
            "Terus pertahankan penglihatan Anda dengan menjaga kesehatan mata secara rutin!"
        )
        keterangan = "Sangat Memuaskan"

    # Menyimpan waktu prediksi
    waktu_akurasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Mendapatkan waktu_userinp dari data.csv
    waktu_userinp = row.get("waktu_userinp", "Tidak Tersedia")  # Mengambil waktu_userinp dari data.csv

    # Menambahkan hasil ke dalam list
    results.append({
        "skor": skor_user,
        "keterangan": keterangan,
        "feedback": feedback,
        "waktu_userinp": waktu_userinp,
        "waktu_akurasi": waktu_akurasi,
    })

# Simpan ke hasil_prediksi.csv tanpa akurasi
hasil = pd.DataFrame(results)

# Cek apakah hasil_prediksi.csv sudah ada
file_exists = os.path.exists("hasil_prediksi.csv")

# Append data ke hasil_prediksi.csv dengan header jika file baru
hasil.to_csv("hasil_prediksi.csv", index=False, mode='w', header=not file_exists)

print("Prediksi berhasil disimpan ke hasil_prediksi.csv")
