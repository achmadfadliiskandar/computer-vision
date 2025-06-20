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
        return "Kurang Memuaskan"
    elif skor == 3:
        return "Memuaskan"
    else:
        return "Sangat Memuaskan"

data["label"] = data["skor"].apply(get_label)

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

# Proses prediksi dan feedback
results = []
for index, row in data.iterrows():
    skor_user = row["skor"]
    X_new = pd.DataFrame([[skor_user]], columns=["skor"])
    prediksi = model.predict(X_new)[0]

    # Feedback sesuai skor
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


    waktu_akurasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    waktu_userinp = row.get("waktu", "Tidak Tersedia")
    # menerima hasil dari model
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