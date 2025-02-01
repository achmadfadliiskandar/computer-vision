import cv2
import time
import json
from urllib.request import urlopen
import mediapipe

# implementasikan mediapipenya
mp_draw = mediapipe.solutions.drawing_utils
mp_hand = mediapipe.solutions.hands



# untuk menentukan lokasi dimana kita berada -- 13
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

vidio = cv2.VideoCapture(0)
vidio.set(cv2.CAP_PROP_FRAME_WIDTH, 870)
vidio.set(cv2.CAP_PROP_FRAME_HEIGHT, 570)
# untuk menentukan lokasi dimana kita berada -- 19

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
            for hand_landmark in result.multi_hand_landmarks:
                wrist = hand_landmark.landmark[mp_hand.HandLandmark.WRIST]
                
                if wrist.x < 0.5:
                    warna = (0, 0, 255)  # Merah (BGR)
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS,landmark_drawing_spec = mp_draw.DrawingSpec(warna))
                else:
                    warna = (0,255,0)   # Hijau (BGR)
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS,landmark_drawing_spec = mp_draw.DrawingSpec(warna))
    # untuk menambahkan waktu dalam camera/vidio-camera
        waktu = time.strftime("%H:%M:%S")
        
    # untuk menambahkan teks dalam vidio/camera
        font = cv2.FONT_HERSHEY_SIMPLEX
        writen = cv2.putText(frame, str(data['city']), (30, 40), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        write = cv2.putText(frame, str(waktu), (30, 82), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    # untuk menampilkan judul dan frame dari siaran kamera
        cv2.imshow("vidio",frame)
    # untuk menghentikan kamera/siaran
        if cv2.waitKey(1) == ord('q'):
            break

# untuk membersihkan resource program
vidio.release()
cv2.destroyAllWindows()