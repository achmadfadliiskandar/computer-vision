import random
import speech_recognition as sr
# judul
print("Tebak Angka 1-5 SPEECH RECOGNITION")

# data angka
data = {
    "satu":1,
    "dua":2,
    "tiga":3,
    "empat":4,
    "lima":5
}
# print(data)
# print(random.choice(data))
kata_acak,datarandoms = random.choice(list(data.items()))


# membuat recognize
recognizer = sr.Recognizer()

# merekam audio input dari microphone
with sr.Microphone() as source:
    print(datarandoms)
    print("tebak angka : ")
    recognizer.adjust_for_ambient_noise(source)
    audio_data = recognizer.listen(source,timeout=5)

while True:
    try:
        # datarandoms = random.choice(data)
        masukan = recognizer.recognize_google(audio_data,language="id-ID").lower()
        print("omongan anda : ",masukan)
        if masukan == kata_acak or masukan == str(datarandoms):
            print("anda benar")
            break
        else:
            print("anda salah ")
            break
    except sr.UnknownValueError:
        print("Maaf Suara Tidak Dikenali")
    except sr.RequestError as e:
        print("Terjadi kesalahan dalam pengenalan suara")