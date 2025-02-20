import cv2
import random
import mediapipe as mp

vidio = cv2.VideoCapture(0)
vidio.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
vidio.set(cv2.CAP_PROP_FRAME_WIDTH,1000)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

data_gambar = ['images/satu.jpeg','images/dua.jpeg','images/tiga.jpeg','images/empat.jpeg','images/lima.jpeg']
acak_gambar = random.randint(0,4)
gambar_random = cv2.imread(data_gambar[acak_gambar])

def hitung_jari(hand_landmark):
    jari_telunjuk = hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y
    jari_tengah = hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y
    jari_manis = hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y
    jari_kelingking = hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y
    jari_jempol = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x > hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
    
    jumlah_jari = sum([jari_telunjuk,jari_tengah,jari_manis,jari_kelingking,jari_jempol])
    return jumlah_jari

with mp_hand.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5,max_num_hands=1) as hands:
    while True:
        ret,frame = vidio.read()
        if not ret:
            break

        # untuk mengeksekusi handlandmarknya
        frame = cv2.flip(frame,1)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = hands.process(frame)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks:
            # print(result.multi_hand_landmarks)
            for i,hand_landmark in enumerate(result.multi_hand_landmarks):
                handedness = result.multi_handedness[i].classification[0].label
                # print(hand_landmark)
                if handedness == "Left":
                    jumlahjari = hitung_jari(hand_landmark)
                    print(f"Jumlah jari: {jumlahjari} | Target: {acak_gambar + 1}")
                    if jumlahjari == acak_gambar + 1:
                        acak_gambar = random.randint(0,4)
                        gambar_random = cv2.imread(data_gambar[acak_gambar])
                else:
                    print("tangan tidak sesuai")

        # untuk ukuran gambar dari folder images/asset gambar angka
        ukuran_gambar = cv2.resize(gambar_random,(200,100))
        tinggi,lebar,_ = gambar_random.shape

        y_offset,x_offset = 10,frame.shape[1] -210
        frame[y_offset:y_offset + 100,x_offset:x_offset + 200] = ukuran_gambar

        cv2.imshow("Tebak Angka 1-5",frame)
        if cv2.waitKey(1) ==  ord('x'):
            break

vidio.release()
cv2.destroyAllWindows()