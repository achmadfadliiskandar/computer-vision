import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import StringVar

# Inisialisasi Mediapipe
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

# Fungsi untuk menentukan jumlah jari yang terangkat
def hitung_jarikiri(hand_landmark):
    jari = [
        hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y,
        hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y,
        hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y,
        hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y,
    ]
    ibu_jari_tip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x
    ibu_jari_ip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
    jari.append(ibu_jari_tip > ibu_jari_ip)
    return sum(jari)
def hitung_jarikanan(hand_landmark):
    jari = [
        hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.INDEX_FINGER_PIP].y,
        hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_PIP].y,
        hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.RING_FINGER_PIP].y,
        hand_landmark.landmark[mp_hand.HandLandmark.PINKY_TIP].y < hand_landmark.landmark[mp_hand.HandLandmark.PINKY_PIP].y,
    ]
    ibu_jari_tip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_TIP].x
    ibu_jari_ip = hand_landmark.landmark[mp_hand.HandLandmark.THUMB_IP].x
    jari.append(ibu_jari_tip < ibu_jari_ip)
    return sum(jari)

# Fungsi untuk menjalankan Hand Tracking
def run_hand_tracking():
    operasi = simbol_input.get()
    vidio = cv2.VideoCapture(0)
    with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
        while True:
            ret, frame = vidio.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            jari_kiri = 0
            jari_kanan = 0
            
            if result.multi_hand_landmarks:
                for hand_landmark in result.multi_hand_landmarks:
                    wrist_x = hand_landmark.landmark[mp_hand.HandLandmark.WRIST].x
                    warna = (0, 0, 255) if wrist_x < 0.5 else (0, 255, 0)
                    mp_draw.draw_landmarks(frame, hand_landmark, mp_hand.HAND_CONNECTIONS,landmark_drawing_spec=mp_draw.DrawingSpec(warna))
                    if wrist_x < 0.5:
                        jari_kiri += hitung_jarikiri(hand_landmark)
                    else:
                        jari_kanan += hitung_jarikanan(hand_landmark)
            
            # Menampilkan hasil operasi
            if operasi == '+':
                total = jari_kiri + jari_kanan
            elif operasi == '-':
                total = jari_kiri - jari_kanan
            elif operasi == '*':
                total = jari_kiri * jari_kanan
            elif operasi == '/':
                total = jari_kiri / jari_kanan if jari_kanan != 0 else "Err"
            else:
                total = "?"
            
            cv2.putText(frame, f"{jari_kiri} {operasi} {jari_kanan} = {total}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Hand Tracking", frame)
            if cv2.waitKey(1) == ord('q'):
                break
    vidio.release()
    cv2.destroyAllWindows()

# GUI Tkinter
root = tk.Tk()
root.title("Hand Tracking Calculator 1-5")
root.geometry("300x200")

simbol_input = StringVar()

label = tk.Label(root, text="Pilih Operasi Aritmatika:")
label.pack(pady=5)

opsi = ['+', '-', '*', '/']
dropdown = tk.OptionMenu(root, simbol_input, *opsi)
dropdown.pack(pady=5)

btn_start = tk.Button(root, text="Mulai", command=run_hand_tracking)
btn_start.pack(pady=10)

root.mainloop()