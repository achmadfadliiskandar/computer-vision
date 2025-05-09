import cv2
# import library waktu
import json
from urllib.request import urlopen
from datetime import datetime
import mediapipe
import pytz
# import library penting


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
vidio.set(cv2.CAP_PROP_FPS, 50)
vidio.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
vidio.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# untuk mengkonfigurasi tampilan vidio -- 25

# fungsi untuk menyimpan jari setiap tangan 27
# tangan kiri
def kiri(hand_landmark):
    # ambil posisi ujung sendi tangan dan masing2 bawah jari
    jari_telunjuk = hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y
    jari_tengah = hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y <  hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y
    jari_manis = hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y
    jari_kelingking = hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y
    jari_jempol = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x > hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
    # hitung semua jari kiri yang terangkat ke kamera
    jariangkatkiri = jari_telunjuk + jari_tengah + jari_manis + jari_kelingking + jari_jempol
    # kembalikan variabel jari angkat kiri dengan return
    return jariangkatkiri
                
# tangan kanan
def kanan(hand_landmark):
    # ambil posisi ujung sendi tangan dan masing2 bawah jari
    jari_telunjuk = hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y
    jari_tengah = hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y <  hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y
    jari_manis = hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y
    jari_kelingking = hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y
    jari_jempol = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x < hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
    # hitung semua jari kanan yang terangkat ke kamera
    jariangkatkanan = jari_telunjuk + jari_tengah + jari_manis + jari_kelingking + jari_jempol
    # kembalikan variabel jari angkat kanan dengan return
    return jariangkatkanan   
# fungsi untuk menyimpan jari setiap tangan 53

# menginisialisasi tangan untuk deteksi serta pelacakan 55
with mp_hand.Hands(min_detection_confidence=0.80,min_tracking_confidence=0.80,max_num_hands=2,model_complexity=1) as hands:
# untuk melakukan siaran vidio secara langsung
    while True:
        ret,frame = vidio.read()
        if not ret:
            break

        frame = cv2.flip(frame,1)

        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # menghitung jari kedua tangan
        jari_kiri = 0
        jari_kanan = 0
        if result.multi_hand_landmarks and result.multi_handedness:
            for i,hand_landmark in enumerate(result.multi_hand_landmarks):
                wrist = result.multi_handedness[i].classification[0].label
                
                if wrist == "Left":
                    warna = (0, 0, 255)  # Merah (BGR)
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS,landmark_drawing_spec = mp_draw.DrawingSpec(warna,thickness=5))
                    jari_kiri += kiri(hand_landmark)
                else:
                    warna = (0,255,0)   # Hijau (BGR)
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS,landmark_drawing_spec = mp_draw.DrawingSpec(warna,thickness=5))
                    jari_kanan += kanan(hand_landmark)
            
            # jumlahkan semua tangan dijari(kanan,kiri)
            cv2.putText(frame, str(jari_kiri), (325, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str("+"), (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 215, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str(jari_kanan), (377, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            
            # menampilkan total tangan yang terangkat dikamera
            total_jari = jari_kiri + jari_kanan
            cv2.putText(frame, str(total_jari), (330, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            
    # untuk menambahkan waktu dalam camera/vidio-camera
        timezone = data.get("timezone","UTC")
        tz = pytz.timezone(timezone)
        waktu = datetime.now(tz).strftime("%H:%M:%S")
        
    # untuk menambahkan teks dalam vidio/camera
        font = cv2.FONT_HERSHEY_SIMPLEX
        writen = cv2.putText(frame, str(data['city']), (30, 40), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        write = cv2.putText(frame, str(waktu), (30, 82), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
    # untuk menampilkan judul dan frame dari siaran kamera
        cv2.imshow("Kamera Deteksi Jari Tangan",frame)
    # untuk menghentikan kamera/siaran
        if cv2.waitKey(1) == ord('q'):
            break

# untuk membersihkan resource program
vidio.release()
cv2.destroyAllWindows()