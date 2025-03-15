import getpass
print("Absensi Python")

datakaryawan = {
    "Nabil": {"NPM": "51422186", "kelas": "3IA13"},
    "Fadli": {"NPM": "50422069", "kelas": "3IA13"},
    "Adrian": {"NPM": "50422102", "kelas": "3IA13"}
}

# Contoh akses data
# print(datakaryawan['50422069'])

# masukin input
dataisi = str(getpass.getpass(prompt='Masukan Data Karyawan : '))
found = False

for key,value in datakaryawan.items():
    if dataisi in value.values():
        print(key,value)
        found = True
if not found:
    print("tidak ada")