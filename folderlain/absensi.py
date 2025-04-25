import getpass
print("Absensi Python")

datakaryawan = {
    "Nabil": {"NPM": "51422186", "kelas": "3IA13","status":"tidak_hadir"},
    "Fadli": {"NPM": "50422069", "kelas": "3IA13","status":"tidak_hadir"},
    "Adrian": {"NPM": "50422102", "kelas": "3IA13","status":"tidak_hadir"},
    "Wisnu": {"NPM": "51422635", "kelas": "3IA19","status":"tidak_hadir"},
}

filename = "data.txt"
with open(filename,"r") as file:
    lines = file.readlines()
# Contoh akses data
# print(datakaryawan['50422069'])

# masukin input
dataisi = str(getpass.getpass(prompt='Masukan Data Karyawan : '))
found = False

for key,value in datakaryawan.items():
    if dataisi in value.values():
        print(f"status {key} hadir")
        with open(filename, "w") as file:
            for line in lines:
                if dataisi in line:
                    line = line.replace("tidak_hadir", "hadir")  # Ubah status
                file.write(line)
        found = True
# jika tidak ada input data dari user
if not found:
    print("tidak ada")