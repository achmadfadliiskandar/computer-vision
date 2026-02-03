import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import speech_recognition as sr
import threading
import csv
from datetime import datetime
import os

class ButaWarnaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screening Buta Warna - Voice Input")
        self.root.geometry("500x650")

        # Dataset Sederhana (Ganti dengan path gambar Anda)
        self.dataset = [
            {"eyeimage": "eyeimage/satu.png", "jawaban": "1"},
            {"eyeimage": "eyeimage/tiga.png", "jawaban": "3"},
            {"eyeimage": "eyeimage/empat.png", "jawaban": "4"},
            {"eyeimage": "eyeimage/lima.png", "jawaban": "5"},
            {"eyeimage": "eyeimage/enam.png", "jawaban": "6"},
            {"eyeimage": "eyeimage/tujuh.png", "jawaban": "7"},
            {"eyeimage": "eyeimage/delapan.png", "jawaban": "8"},
            {"eyeimage": "eyeimage/sembilan.png", "jawaban": "9"},
            {"eyeimage": "eyeimage/duabelas.png", "jawaban": "12"},
            {"eyeimage": "eyeimage/limabelas.png", "jawaban": "15"},
            {"eyeimage": "eyeimage/enambelas.png", "jawaban": "16"},
            {"eyeimage": "eyeimage/duasembilan.png", "jawaban": "29"},
            {"eyeimage": "eyeimage/duaenam.png", "jawaban": "26"},
            {"eyeimage": "eyeimage/tigalima.png", "jawaban": "35"},
            {"eyeimage": "eyeimage/tigadelapan.png", "jawaban": "38"},
            {"eyeimage": "eyeimage/empatdua.png", "jawaban": "42"},
            {"eyeimage": "eyeimage/empatlima.png", "jawaban": "45"},
            {"eyeimage": "eyeimage/limasatu.png", "jawaban": "51"},
            {"eyeimage": "eyeimage/limatujuh.png", "jawaban": "57"},
            {"eyeimage": "eyeimage/enamsembilan.png", "jawaban": "69"},
            {"eyeimage": "eyeimage/tujuhtiga.png", "jawaban": "73"},
            {"eyeimage": "eyeimage/tujuhempat.png", "jawaban": "74"},
            {"eyeimage": "eyeimage/sembilanenam.png", "jawaban": "96"},
            {"eyeimage": "eyeimage/sembilantujuh.png", "jawaban": "97"}
        ]
        
        self.index_soal = 0
        self.skor = 0
        
        # Mapping Suara
        self.mapping_angka = {
            # Satuan
            "angka satu": "1", "angka dua": "2", "angka tiga": "3", 
            "angka empat": "4", "angka lima": "5", "angka enam": "6", 
            "angka tujuh": "7", "angka delapan": "8", "angka sembilan": "9",
            
            # Belasan (Dari dataset Anda)
            "angka sepuluh": "10", "angka sebelas": "11", "angka dua belas": "12",
            "angka tiga belas": "13", "angka empat belas": "14", "angka lima belas": "15",
            "angka enam belas": "16", "angka tujuh belas": "17", "angka delapan belas": "18",
            "angka sembilan belas": "19",

            # Puluhan yang ada di dataset plate Anda
            "angka dua puluh enam": "26", "angka dua puluh sembilan": "29",
            "angka tiga puluh lima": "35", "angka tiga puluh delapan": "38",
            "angka empat puluh dua": "42", "angka empat puluh lima": "45",
            "angka lima puluh satu": "51", "angka lima puluh tujuh": "57",
            "angka enam puluh sembilan": "69", "angka tujuh puluh tiga": "73",
            "angka tujuh puluh empat": "74", "angka sembilan puluh enam": "96",
            "angka sembilan puluh tujuh": "97", "angka seratus": "100",
            
            # Tambahan variasi nol
            "angka nol": "0", "angka kosong": "0"
        }

        # UI Elements
        self.label_instruksi = tk.Label(root, text="Sebutkan angka yang Anda lihat!", font=("Arial", 12))
        self.label_instruksi.pack(pady=10)

        self.canvas = tk.Canvas(root, width=300, height=300, bg="gray")
        self.canvas.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Siap", fg="blue")
        self.status_label.pack(pady=5)

        self.btn_bicara = tk.Button(root, text="Mulai Bicara", command=self.mulai_thread_suara, 
                                   bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        self.btn_bicara.pack(pady=20)

        self.hasil_label = tk.Label(root, text="Hasil Suara: -", font=("Arial", 10, "italic"))
        self.hasil_label.pack(pady=10)

        self.load_gambar()

    def load_gambar(self):
        # Logika menampilkan gambar
        if self.index_soal < len(self.dataset):
            try:
                img_path = self.dataset[self.index_soal]["eyeimage"]
                img = Image.open(img_path)
                img = img.resize((300, 300))
                self.photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(150, 150, image=self.photo)
            except:
                self.canvas.create_text(150, 150, text=f"Gambar {self.index_soal+1} tidak ditemukan")
        else:
            self.tampilkan_diagnosa()

    def mulai_thread_suara(self):
        # Jalankan suara di thread berbeda agar UI tidak membeku (freeze)
        self.btn_bicara.config(state="disabled")
        threading.Thread(target=self.proses_suara).start()

    def proses_suara(self):
        r = sr.Recognizer()
        r.pause_threshold = 0.5
        r.energy_threshold = 150
        r.dynamic_energy_threshold = True
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            self.status_label.config(text="Status: Katakan 'Angka [Nomor]...", fg="red")
            try:
                audio = r.listen(source, timeout=4, phrase_time_limit=3)
                self.status_label.config(text="Status: Memproses...", fg="orange")
                
                # Menggunakan Google Speech Recognition (Membutuhkan Internet)
                text = r.recognize_google(audio, language="id-ID").lower()
                self.hasil_label.config(text=f"Hasil Suara: {text}")

                # Cek Jawaban
                jawaban_user = self.mapping_angka.get(text, text)
                kunci = self.dataset[self.index_soal]["jawaban"]

                if jawaban_user == kunci:
                    self.skor += 1
                
                self.index_soal += 1
                self.root.after(1000, self.lanjut_soal)

            except Exception as e:
                messagebox.showerror("Error", "Suara tidak terdengar atau koneksi terputus")
            
            self.btn_bicara.config(state="normal")
            self.status_label.config(text="Status: Siap", fg="blue")

    def lanjut_soal(self):
        self.hasil_label.config(text="Hasil Suara: -")
        self.load_gambar()
    
    def simpan_ke_csv(self, skor, keterangan):
        file_name = 'data.csv'
        header = ['skor', 'keterangan', 'waktu']
        
        # Ambil waktu sekarang (Format: Jam:Menit:Detik)
        waktu_sekarang = datetime.now().strftime("%H:%M:%S")
        
        file_exists = os.path.isfile(file_name)
        
        with open(file_name, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            
            # Simpan hanya 3 kolom
            writer.writerow([skor, keterangan, waktu_sekarang])

    def tampilkan_diagnosa(self):
        # Mapping Skor (Tanpa IF)
        DIAGNOSA_MAP = (
            ["buta warna total"] * 10 +    # 0-9
            ["buta warna parsial"] * 12 + # 10-21
            ["normal"] * 3                # 22-24
        )
        
        idx = min(self.skor, 24)
        hasil_kategori = DIAGNOSA_MAP[idx]
        
        # Panggil fungsi simpan (Hanya kirim 2 argumen)
        self.simpan_ke_csv(self.skor, hasil_kategori)
        
        messagebox.showinfo("Hasil Akhir", 
                            f"Skor: {self.skor}\n"
                            f"Kategori: {hasil_kategori}\n\n"
                            "Data tersimpan ke data.csv")
        
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ButaWarnaApp(root)
    root.mainloop()