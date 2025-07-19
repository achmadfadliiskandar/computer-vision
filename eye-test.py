import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os, random, csv, datetime, subprocess
import pandas
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
# library' penting diatas

# Data dan variabel global
jumlah_soal = 0
skor = 0
maks_soal = 5

# kumpulan soal' untuk pengujian mata
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
        img = Image.open(soal["eyeimage"]).resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        input_entry.delete(0, tk.END)
    else:
        print(f"Gambar tidak ditemukan: {soal['eyeimage']}")

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

        keterangan = "kurang memuaskan" if skor <= 2 else "memuaskan" if skor == 3 else "sangat memuaskan"
        keterangan_label.config(text=f"Kategori: {keterangan.capitalize()}", fg="purple")

        waktu = datetime.datetime.now().strftime("%X")
        filename = "data.csv"
        fieldnames = ['skor', 'keterangan', 'waktu']
        with open(filename, "a", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(filename).st_size == 0:
                writer.writeheader()
            writer.writerow({'skor': skor, 'keterangan': keterangan, 'waktu': waktu})

        with open(filename, newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        print(tabulate(data[1:], headers=data[0], tablefmt="grid"))


        if os.path.exists("eyeimage/terimakasih.png"):
            img = Image.open("eyeimage/terimakasih.png").resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
    # pengaturan ukuran reset button
        reset_button.pack(pady=10)
        cek_feedback.pack(pady=10)

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
    cek_feedback.pack_forget()

    # lakukan random soal secara otomatis
    randomsoal()

def feedback():
    try:
        subprocess.run(['python', 'modelhashihara.py'], check=True)
        data_hasil = pandas.read_csv("hasil_prediksi.csv")
        last_entry = data_hasil.iloc[-1]
        feedback_last = last_entry["feedback"]
        keterangan_last = last_entry["keterangan"]
        text = f"Keterangan: {keterangan_last}\nFeedback: {feedback_last}"
        messagebox.showinfo("Feedback", text)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mendapatkan feedback: {e}")

# Fungsi untuk mengekspor ke PDF
def export_to_pdf():
    try:
        filename = "hasil_tes_5_terakhir.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 50, "Laporan 5 Tes Terakhir - Buta Warna")

        c.setFont("Helvetica", 12)
        y = height - 90

        df = pandas.read_csv("hasil_prediksi.csv")
        last_five = df.tail(5)  # ambil 5 data terakhir

        for idx, row in last_five.iterrows():
            lines = [
                f"Tanggal Tes    : {row['waktu_userinp']}",
                f"Waktu Prediksi : {row['waktu_akurasi']}",
                f"Skor Jawaban   : {row['skor']}",
                f"Keterangan     : {row['keterangan']}",
                f"Feedback       :",
            ]

            for line in lines:
                c.drawString(50, y, line)
                y -= 20

            feedback_lines = str(row['feedback']).split('. ')
            for line in feedback_lines:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = height - 90
                c.drawString(70, y, f"- {line.strip()}")
                y -= 20

            y -= 30  # spasi antar entri

            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 90

        c.save()
        messagebox.showinfo("Berhasil", f"5 hasil terakhir berhasil disimpan ke {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan ke PDF: {e}")



# Fungsi untuk mengatur tampilan konten
def show_home():
    for widget in content_frame.winfo_children():
        widget.destroy()
    # Hapus sidebar dari layar jika ada
    sidebar.pack(side="left", fill="y")


    # Reset data logika saja
    global skor, jumlah_soal, soal_tersisa
    skor = 0
    jumlah_soal = 0
    soal_tersisa = list_soal.copy()

    global image_label, input_entry, kotakjawaban, hasil_label, keterangan_label, reset_button, cek_feedback

    judul = tk.Label(content_frame, text="Test Buta Warna", font=("Helvetica", 18, "bold"))
    judul.pack(pady=10)

    image_label = tk.Label(content_frame)
    image_label.pack(pady=10)

    tk.Label(content_frame, text="Angka Yang Kamu Lihat:").pack()
    input_entry = tk.Entry(content_frame, width=20)
    input_entry.pack(pady=5)

    kotakjawaban = tk.Button(content_frame, text="Submit", command=cek_jawaban)
    kotakjawaban.pack(pady=10)

    hasil_label = tk.Label(content_frame, text="", font=("Helvetica", 12))
    hasil_label.pack()

    keterangan_label = tk.Label(content_frame, text="", font=("Helvetica", 12))
    keterangan_label.pack()

    reset_button = tk.Button(content_frame, text="Reset", command=reset_game)
    reset_button.pack_forget()

    cek_feedback = tk.Button(content_frame, text="Get Feedback", command=feedback)
    cek_feedback.pack_forget()

    # Panggil random soal terakhir setelah semua elemen GUI dibuat
    randomsoal()


def show_dashboard():
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="📊 Dashboard", font=("Helvetica", 18, "bold")).pack(pady=10)

    try:
        df = pandas.read_csv("data.csv")
        if df.empty or 'keterangan' not in df.columns:
            raise ValueError("Data kosong atau kolom 'keterangan' tidak ditemukan.")

        df = df.dropna(subset=['keterangan'])
        category_counts = df['keterangan'].value_counts()

        # --- GRAFIK BATANG SAJA ---
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.bar(category_counts.index, category_counts.values, color=['green', 'red', 'orange'])
        ax.set_title("Statistik Hasil Tes")
        ax.set_ylabel("Jumlah")
        ax.set_xlabel("Kategori")

        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # --- TABEL RINGKASAN DATA ---
        tk.Label(content_frame, text="Ringkasan Data", font=("Helvetica", 14, "bold")).pack(pady=(20, 5))

        header = tk.Frame(content_frame)
        header.pack()
        tk.Label(header, text="Kategori", width=20, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        tk.Label(header, text="Jumlah", width=10, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        for kategori in ["sangat memuaskan", "memuaskan", "kurang memuaskan"]:
            jumlah = category_counts.get(kategori, 0)
            row = tk.Frame(content_frame)
            row.pack()
            tk.Label(row, text=kategori, width=20).pack(side="left", padx=5)
            tk.Label(row, text=str(jumlah), width=10).pack(side="left", padx=5)

        row_total = tk.Frame(content_frame)
        row_total.pack(pady=(5, 10))
        tk.Label(row_total, text="Total Data", width=20, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        tk.Label(row_total, text=str(df.shape[0]), width=10, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        # --- TOMBOL EXPORT PDF ---
        tk.Button(content_frame, text="Export 5 Feedback terakhir ke PDF", command=export_to_pdf).pack(pady=10)

    except FileNotFoundError:
        tk.Label(content_frame, text="File data.csv tidak ditemukan.", font=("Helvetica", 12), fg="red").pack(pady=20)
    except ValueError as ve:
        tk.Label(content_frame, text=f"Data Error: {ve}", font=("Helvetica", 12), fg="red").pack(pady=20)
    except Exception as e:
        tk.Label(content_frame, text=f"Terjadi kesalahan: {e}", font=("Helvetica", 12), fg="red").pack(pady=20)



def show_settings():
    for widget in content_frame.winfo_children():
        widget.destroy()

    def apply_settings():
        new_theme = theme_var.get()
        root.config(bg=new_theme)
        sidebar.config(bg=new_theme)  # Apply theme to sidebar as well
        content_frame.config(bg=new_theme)

    tk.Label(content_frame, text="Settings", font=("Helvetica", 16, "bold")).pack(pady=10)

    tk.Label(content_frame, text="Ubah Warna Tema:").pack()
    theme_var = tk.StringVar(value="white")
    tk.OptionMenu(content_frame, theme_var, "white", "lightgray", "lightblue", "lightgreen").pack(pady=5)

    tk.Button(content_frame, text="Change Settings", command=apply_settings).pack(pady=10)


def start_application():
    """Removes the start screen and shows the main application."""
    for widget in root.winfo_children():
        widget.destroy() # Clear all widgets from the root window

    # Recreate sidebar and content_frame for the main application
    global sidebar, content_frame
    sidebar = tk.Frame(root, bg="#2c3e50", width=150)
    sidebar.pack(side="left", fill="y")

    btn_home = tk.Button(sidebar, text="Home", command=show_home, fg="white", bg="#34495e", relief="flat")
    btn_home.pack(fill="x", pady=5, padx=5)

    btn_visualisasi = tk.Button(sidebar, text="Dashboard", command=show_dashboard, fg="white", bg="#34495e", relief="flat")
    btn_visualisasi.pack(fill="x", pady=5, padx=5)

    btn_settings = tk.Button(sidebar, text="Pengaturan", command=show_settings, fg="white", bg="#34495e", relief="flat")
    btn_settings.pack(fill="x", pady=5, padx=5)

    content_frame = tk.Frame(root)
    content_frame.pack(side="right", expand=True, fill="both")

    show_home() # Now show the actual home screen of the application


def show_start_screen():
    """Displays the initial welcome screen with a start button."""
    global content_frame # Make content_frame globally accessible to destroy its widgets

    # Clear any existing widgets on the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame for the start screen content, taking up the whole window
    start_frame = tk.Frame(root, bg="white")
    start_frame.pack(expand=True, fill="both")

    tk.Label(start_frame, text="Selamat Datang di Aplikasi Tes Buta Warna",
             font=("Helvetica", 20, "bold"), bg="white").pack(pady=50)

    start_button = tk.Button(start_frame, text="Mulai", command=start_application,
                             font=("Helvetica", 16, "bold"), bg="#D9D9D9", fg="black",
                             relief="raised", padx=20, pady=10)
    start_button.pack(pady=30)


# GUI Utama
root = tk.Tk()
root.title("Test Buta Warna")
root.geometry("900x700")

# Initialize content_frame as a placeholder before it's properly defined in start_application
content_frame = tk.Frame(root)
# Initially, the sidebar is not packed, it will be packed by start_application
sidebar = tk.Frame(root) # Placeholder, will be recreated later

# Tampilkan halaman mulai saat start
show_start_screen()

# tampilan mutlak program
def on_exit():
    if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
        plt.close('all')
        root.destroy()

# Di akhir program
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
