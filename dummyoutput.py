import pandas as pd
import random
import os

# Jumlah data dummy yang ingin ditambahkan
jumlah_data = 10

# Generate skor acak antara 1 sampai 5 dan tentukan keterangan
data_dummy = []
for _ in range(jumlah_data):
    skor = random.randint(1, 5)
    keterangan = (
        "kurang menguasai" if skor <= 2
        else "menguasai" if skor == 3
        else "sangat menguasai"
    )
    data_dummy.append({"skor": skor, "keterangan": keterangan})

# Buat DataFrame dari data dummy
df_dummy = pd.DataFrame(data_dummy)

# Cek apakah file data.csv sudah ada
file_path = "data.csv"
file_exists = os.path.exists(file_path)

# Tambahkan data ke file, jika belum ada file maka akan dibuat
df_dummy.to_csv(file_path, index=False, mode='a', header=not file_exists)

print(f"{jumlah_data} data dummy berhasil ditambahkan ke {file_path}")