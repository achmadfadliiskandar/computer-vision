from gtts import gTTS
import playsound
masukan_suara = input("teks ini kedalam vidio : ")
tts = gTTS(masukan_suara,lang='id',slow=False)
tts.save(f'audio/{masukan_suara}.mp3')
playsound.playsound(f"audio/{masukan_suara}.mp3")
