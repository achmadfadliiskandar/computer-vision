import tkinter as ttk
from PIL import Image, ImageTk
import os
import random
from tkinter import messagebox
import csv
from tabulate import tabulate

# Tampilkan angka point(skor) jika benar
jumlah_soal = 0
skor = 0
maks_soal = 5

# Data gambar dan jawaban
list_soal = [
    {"eyeimage": "eyeimage/tujuh.jpg", "jawaban": "7"},
    {"eyeimage": "eyeimage/duabelas.png", "jawaban": "12"},
    {"eyeimage": "eyeimage/sembilanbelas.jpg", "jawaban": "19"},
    {"eyeimage": "eyeimage/tujuhempat.png", "jawaban": "74"},
    {"eyeimage": "eyeimage/sembilanenam.jpeg", "jawaban": "96"},
    {"eyeimage": "eyeimage/dualima.png", "jawaban": "25"},
    {"eyeimage": "eyeimage/enamlima.png", "jawaban": "65"},
    {"eyeimage": "eyeimage/tigatiga.png", "jawaban": "33"},
    {"eyeimage": "eyeimage/limatiga.png", "jawaban": "53"},
    {"eyeimage": "eyeimage/sembilansembilan.png", "jawaban": "99"},
    {"eyeimage": "eyeimage/empatpuluh.png", "jawaban": "40"},
    {"eyeimage": "eyeimage/delapanempat.png", "jawaban": "84"},
]

soal_tersisa = list_soal.copy()

def randomsoal():
    global img_tk, soal, soal_tersisa
    if not soal_tersisa:
        soal_tersisa = list_soal.copy()
    soal = random.choice(soal_tersisa)
    soal_tersisa.remove(soal)
    if os.path.exists(soal["eyeimage"]):
        img = Image.open(soal["eyeimage"])
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        input_entry.delete(0, ttk.END)
    else:
        print(f"File gambar tidak ditemukan: {soal['eyeimage']}")

def cek_jawaban():
    global skor, jumlah_soal
    jawaban_user = input_entry.get()
    if not jawaban_user.isnumeric():
        messagebox.showwarning("Input error", "Jawaban harus berupa angka dan jangan kosong")
        return
    jumlah_soal += 1
    if jawaban_user == soal["jawaban"]:
        hasil_label.config(text="✅ Benar!", fg="green")
        skor += 1
    else:
        hasil_label.config(text=f"❌ Salah! Jawaban: {soal['jawaban']}", fg="red")

    if jumlah_soal >= maks_soal:
        hasil_label.config(text=f"Tes Selesai! skor akhir : {skor} dari {maks_soal}", fg="blue")
        kotakjawaban.config(state="disabled")
        input_entry.config(state="disabled")

        keterangan = "kurang menguasai" if skor <= 2 else "menguasai" if skor == 3 else "sangat menguasai"
        keterangan_label.config(text=f"Kategori: {keterangan.capitalize()}", fg="purple")

        fieldnames = ['skor', 'keterangan']
        dbcsv = {'skor': skor, 'keterangan': keterangan}
        filename = "data.csv"
        file_exists = os.path.exists(filename)
        with open(filename, "a", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(dbcsv)

        with open(filename, newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        print(tabulate(data[1:], headers=data[0], tablefmt="grid"))

        # Tampilkan gambar terimakasih jika ada
        if os.path.exists("eyeimage/terimakasih.png"):
            img = Image.open("eyeimage/terimakasih.png")
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
        else:
            print("Gambar terimakasih tidak ada")

        reset_button.pack(pady=10)
    else:
        randomsoal()

def reset_game():
    global skor, jumlah_soal, soal_tersisa
    skor = 0
    jumlah_soal = 0
    soal_tersisa = list_soal.copy()
    kotakjawaban.config(state="normal")
    input_entry.config(state="normal")
    hasil_label.config(text="")
    keterangan_label.config(text="")
    reset_button.pack_forget()
    randomsoal()

# GUI
root = ttk.Tk()
root.title("Test Hashihara")
root.geometry("500x550")

judul = ttk.Label(root, text="Test Buta Warna", font=("Helvetica", 18, "bold"))
judul.pack(pady=10)

image_label = ttk.Label(root)
image_label.pack(pady=10)

input_label = ttk.Label(root, text="Angka Yang Kamu Lihat: ")
input_label.pack()
input_entry = ttk.Entry(root, width=20)
input_entry.pack(pady=5)

kotakjawaban = ttk.Button(root, text="Submit", command=cek_jawaban)
kotakjawaban.pack(pady=10)

hasil_label = ttk.Label(root, text="", font=("Helvetica", 12))
hasil_label.pack()

keterangan_label = ttk.Label(root, text="", font=("Helvetica", 12))
keterangan_label.pack()

reset_button = ttk.Button(root, text="Reset", command=reset_game)
reset_button.pack_forget()

randomsoal()
root.mainloop()
