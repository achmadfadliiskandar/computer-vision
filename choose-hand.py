import cv2
import time
import json
from urllib.request import urlopen
import mediapipe

mp_draw = mediapipe.solutions.drawing_utils
mp_hand = mediapipe.solutions.hands

# Memilih tangan yang akan dideteksi
pilihan_tangan = input("Pilih tangan yang akan dideteksi (kanan/kiri): ").lower()

# Menentukan lokasi
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

vidio = cv2.VideoCapture(0)
vidio.set(cv2.CAP_PROP_FRAME_WIDTH, 870)
vidio.set(cv2.CAP_PROP_FRAME_HEIGHT, 570)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = vidio.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmark, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                label = handedness.classification[0].label.lower()  # 'left' atau 'right' / kiri' atau 'kanan' 

                if (pilihan_tangan == 'kanan' and label == 'right') or (pilihan_tangan == 'kiri' and label == 'left'):
                    wrist = hand_landmark.landmark[mp_hand.HandLandmark.WRIST]

                    if wrist.x < 0.5:
                        warna = (0, 0, 255)  # Merah (BGR)
                        # ambil posisi ujung sendi tangan dan masing2 bawah jari
                        jari_telunjuk = hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y
                        jari_tengah = hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y <  hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y
                        jari_manis = hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y
                        jari_kelingking = hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y

                        # Logika untuk mengecek jempol (x)
                        ibu_jari_tip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x
                        ibu_jari_ip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
                        jari_jempol = ibu_jari_tip > ibu_jari_ip if wrist.x < 0.5 else ibu_jari_tip < ibu_jari_ip

                        # Hitung jari yang terangkat/terlihat dividio camera
                        jariangkat = jari_telunjuk + jari_tengah + jari_manis + jari_kelingking + jari_jempol
                        cv2.putText(frame,str(jariangkat), (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, warna, 2, cv2.LINE_AA)
                        mp_draw.draw_landmarks(
                        frame, hand_landmark, mp_hand.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_draw.DrawingSpec(color=warna, thickness=2, circle_radius=4)
                        )
                    else:
                        warna = (0, 255, 0)  # Hijau (BGR)
                        # ambil posisi ujung sendi tangan dan masing2 bawah jari
                        jari_telunjuk = hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y
                        jari_tengah = hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y <  hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y
                        jari_manis = hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y
                        jari_kelingking = hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y

                        # Logika untuk mengecek jempol (x)
                        ibu_jari_tip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x
                        ibu_jari_ip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
                        jari_jempol = ibu_jari_tip > ibu_jari_ip if wrist.x < 0.5 else ibu_jari_tip < ibu_jari_ip

                        # Hitung jari yang terangkat/terlihat dividio camera
                        jariangkat = jari_telunjuk + jari_tengah + jari_manis + jari_kelingking + jari_jempol
                        cv2.putText(frame,str(jariangkat), (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, warna, 2, cv2.LINE_AA)

                        mp_draw.draw_landmarks(
                            frame, hand_landmark, mp_hand.HAND_CONNECTIONS,
                            landmark_drawing_spec=mp_draw.DrawingSpec(color=warna, thickness=2, circle_radius=4)
                        )
                elif (pilihan_tangan not in ['kanan','kiri']) or (pilihan_tangan == 'kanan' not in label == 'right') and (pilihan_tangan == 'kiri' not in label == 'left'):
                    cv2.putText(frame,str('salah input ya!!'), (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

        waktu = time.strftime("%H:%M:%S")
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(data['city']), (30, 40), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str(waktu), (30, 82), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("vidio", frame)

        if cv2.waitKey(1) == ord('q'):
            break

vidio.release()
cv2.destroyAllWindows()