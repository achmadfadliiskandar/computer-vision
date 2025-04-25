import cv2
import mediapipe as mp

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Buka kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

zoom = 1.0  # Zoom level awal
target_zoom = 1.0  # Zoom yang akan dicapai berdasarkan jarak tangan

def get_hand_box_size(landmarks, img_width, img_height):
    xs = [lm.x * img_width for lm in landmarks]
    ys = [lm.y * img_height for lm in landmarks]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    return width * height  # area

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # Proses MediaPipe
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Deteksi tangan & ukur ukuran relatifnya
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            area = get_hand_box_size(hand_landmarks.landmark, w, h)

            # Tentukan target zoom berdasarkan area tangan
            if area < 3000:
                target_zoom = 1.8
            elif area < 6000:
                target_zoom = 1.5
            else:
                target_zoom = 1.0

    else:
        target_zoom = 1.0  # tidak ada tangan → reset zoom

    # Smooth zoom (supaya tidak langsung lompat)
    zoom += (target_zoom - zoom) * 0.1

    # Simulasi zoom digital (crop tengah lalu resize)
    if zoom != 1.0:
        center_x, center_y = w // 2, h // 2
        new_w, new_h = int(w / zoom), int(h / zoom)
        left = max(center_x - new_w // 2, 0)
        top = max(center_y - new_h // 2, 0)
        right = min(center_x + new_w // 2, w)
        bottom = min(center_y + new_h // 2, h)
        frame = frame[top:bottom, left:right]
        frame = cv2.resize(frame, (w, h))

    cv2.imshow("Zoom Otomatis - MediaPipe", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()