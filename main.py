import cv2
import time
import json
from urllib.request import urlopen
import mediapipe
# import important library


# implementasikan mediapipenya
mp_draw = mediapipe.solutions.drawing_utils
mp_hand = mediapipe.solutions.hands
# implementasikan bentuk tangan dan gambar tanganya

# untuk menentukan lokasi dimana kita berada -- 13
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
# untuk menentukan lokasi dimana kita berada -- 18

# untuk mengkonfigurasi tampilan vidio -- 20
vidio = cv2.VideoCapture(0)
vidio.set(cv2.CAP_PROP_FPS, 30)
vidio.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
vidio.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# untuk mengkonfigurasi tampilan vidio -- 25

# fungsi untuk menyimpan jari setiap tangan 27
# kiri
def kiri(hand_landmark):
    # ambil posisi ujung sendi tangan dan masing2 bawah jari
    jari_telunjuk = hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y
    jari_tengah = hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y <  hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y
    jari_manis = hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y
    jari_kelingking = hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y

    # Logika untuk mengecek jempol (x)
    ibu_jari_tip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x
    ibu_jari_ip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
    jari_jempol = ibu_jari_tip > ibu_jari_ip if wrist.x < 0.5 else ibu_jari_tip < ibu_jari_ip
    jariangkatkiri = jari_telunjuk + jari_tengah + jari_manis + jari_kelingking + jari_jempol
    # cv2.putText(frame,str(jariangkatkiri), (325, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, warna, 2, cv2.LINE_AA)
    return jariangkatkiri
                
# kanan
def kanan(hand_landmark):
    # ambil posisi ujung sendi tangan dan masing2 bawah jari
    jari_telunjuk = hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y
    jari_tengah = hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y <  hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y
    jari_manis = hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y
    jari_kelingking = hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y

    # Logika untuk mengecek jempol (x)
    ibu_jari_tip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x
    ibu_jari_ip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
    jari_jempol = ibu_jari_tip > ibu_jari_ip if wrist.x < 0.5 else ibu_jari_tip < ibu_jari_ip
    jariangkatkanan = jari_telunjuk + jari_tengah + jari_manis + jari_kelingking + jari_jempol
    # cv2.putText(frame,str(jariangkatkanan), (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, warna, 2, cv2.LINE_AA)
    return jariangkatkanan   
# fungsi untuk menyimpan jari setiap tangan 57 

# melakukan pendeteksian kamera untuk tangan yang berada di kamera
with mp_hand.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:
# untuk melakukan siaran vidio secara langsung
    while True:
        ret,frame = vidio.read()
        if not ret:
            break

        frame = cv2.flip(frame,1)

        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks:
            # menghitung jari kedua tangan
            jari_kiri = 0
            jari_kanan = 0
            for hand_landmark in result.multi_hand_landmarks:
                wrist = hand_landmark.landmark[mp_hand.HandLandmark.WRIST]
                
                if wrist.x < 0.5:
                    warna = (0, 0, 255)  # Merah (BGR)
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS,landmark_drawing_spec = mp_draw.DrawingSpec(warna))
                    jari_kiri += kiri(hand_landmark)
                else:
                    warna = (0,255,0)   # Hijau (BGR)
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS,landmark_drawing_spec = mp_draw.DrawingSpec(warna))
                    jari_kanan += kanan(hand_landmark)
            
            # jumlahkan semua tangan dijari(kanan,kiri)
            cv2.putText(frame, str(jari_kiri), (325, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str("+"), (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 215, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str(jari_kanan), (377, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            
            # menampilkan total tangan yang terangkat dikamera
            total_jari = jari_kiri + jari_kanan
            cv2.putText(frame, str(total_jari), (330, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            
    # untuk menambahkan waktu dalam camera/vidio-camera
        waktu = time.strftime("%H:%M:%S")
        
    # untuk menambahkan teks dalam vidio/camera
        font = cv2.FONT_HERSHEY_SIMPLEX
        writen = cv2.putText(frame, str(data['city']), (30, 40), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        write = cv2.putText(frame, str(waktu), (30, 82), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
    # untuk menampilkan judul dan frame dari siaran kamera
        cv2.imshow("vidio",frame)
    # untuk menghentikan kamera/siaran
        if cv2.waitKey(1) == ord('q'):
            break

# untuk membersihkan resource program
vidio.release()
cv2.destroyAllWindows()