import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime
import os

# --- Load data.csv ---
if not os.path.exists("data.csv"):
    print("Error: File 'data.csv' tidak ditemukan. Harap jalankan aplikasi utama untuk membuat data terlebih dahulu.")
    exit()

data = pd.read_csv("data.csv")

# Mengubah data sesuai kebutuhan model
def get_label(keterangan):
    if keterangan == "buta warna total":
        return "buta warna total"
    elif keterangan == "buta warna parsial":
        return "buta warna parsial"
    else: # normal
        return "normal"

data["label"] = data["keterangan"].apply(get_label)

# Fitur dan Label
X = data[["skor"]]
y = data["label"]

# Jika data kurang dari 2, tidak bisa split
if len(data) < 2:
    print("Jumlah data kurang dari 2. Model tetap dilatih, namun akurasi tidak dihitung.")
    X_train = X
    y_train = y
    X_test = X
    y_test = y
    skip_accuracy = True
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    skip_accuracy = False

# Melatih model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Hitung akurasi jika memungkinkan
if not skip_accuracy:
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"Akurasi Model: {accuracy:.2f}%")
else:
    accuracy = None

# Proses prediksi dan feedback untuk semua data di CSV
results = []
for index, row in data.iterrows():
    skor_user = row["skor"]
    X_new = pd.DataFrame([[skor_user]], columns=["skor"])
    # Menggunakan hasil prediksi model untuk menentukan kategori
    prediksi = model.predict(X_new)[0]

    # Menentukan feedback berdasarkan hasil prediksi model
    if prediksi == "buta warna total":
        keterangan = "buta warna total"
        feedback = (
            "Hasil tes menunjukkan bahwa Anda mengalami kesulitan dalam membedakan warna. "
            "Kami menyarankan agar Anda berkonsultasi dengan dokter spesialis mata untuk pemeriksaan lebih lanjut. "
            "Tes lebih lanjut dapat membantu mendapatkan diagnosis yang lebih akurat."
        )
    elif prediksi == "buta warna parsial":
        keterangan = "buta warna parsial"
        feedback = (
            "Hasil tes menunjukkan bahwa Anda memiliki kemampuan penglihatan warna yang cukup baik. "
            "Namun, mungkin ada beberapa kondisi atau warna yang masih cukup menantang untuk Anda. "
            "Kami sarankan untuk terus berlatih dan tetap menjaga kesehatan mata."
        )
    else: # prediksi == "normal"
        keterangan = "normal"
        feedback = (
            "Hasil tes menunjukkan bahwa kemampuan penglihatan warna Anda sangat baik. "
            "Anda dapat membedakan warna dengan jelas dan tajam dalam berbagai kondisi. "
            "Terus pertahankan penglihatan Anda dengan menjaga kesehatan mata secara rutin!"
        )
        

    waktu_akurasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    waktu_userinp = row.get("waktu", "Tidak Tersedia")
    
    results.append({
        "skor": skor_user,
        "keterangan": keterangan,
        "feedback": feedback,
        "waktu_userinp": waktu_userinp,
        "waktu_akurasi": waktu_akurasi,
    })

# Simpan hasil prediksi
hasil = pd.DataFrame(results)
hasil.to_csv("hasil_prediksi.csv", index=False)
print("Prediksi berhasil disimpan ke hasil_prediksi.csv")