import cv2
import numpy as np
import math

try:
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_draw
except:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

# Setup 2 Tangan
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)

# Penyimpanan terpisah untuk tiap ID tangan agar tidak tercampur
all_strokes = [] 
active_strokes = {} # Dictionary untuk melacak coretan tiap tangan {hand_id: [points]}

cap = cv2.VideoCapture(0)

print("Mode Dual-Hand Painting Aktif!")
print("- Tempelkan Telunjuk & Tengah untuk MELUKIS.")
print("- Tekan 'c' untuk HAPUS, 'q' untuk KELUAR.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Kumpulan ID tangan yang terdeteksi di frame ini
    present_ids = []

    if results.multi_hand_landmarks:
        # enumerate untuk membedakan Tangan 1 dan Tangan 2
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            present_ids.append(idx)
            
            # Gambar Skeleton
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Koordinat jari
            itip = hand_landmarks.landmark[8]
            mtip = hand_landmarks.landmark[12]
            ix, iy = int(itip.x * w), int(itip.y * h)
            mx, my = int(mtip.x * w), int(mtip.y * h)

            # Cek Jarak (Saklar)
            distance = math.hypot(mx - ix, my - iy)

            if distance < 45:
                # Jika tangan ini belum punya jalur coretan, buat baru
                if idx not in active_strokes:
                    active_strokes[idx] = []
                active_strokes[idx].append((ix, iy))
                cv2.circle(frame, (ix, iy), 10, (0, 255, 0), cv2.FILLED)
            else:
                # Jika jari dipisahkan, simpan coretan tangan tersebut ke arsip
                if idx in active_strokes and len(active_strokes[idx]) > 0:
                    all_strokes.append(active_strokes[idx])
                    active_strokes[idx] = []
                cv2.circle(frame, (ix, iy), 10, (0, 0, 255), cv2.FILLED)

    # Bersihkan stroke tangan yang tiba-tiba hilang dari kamera
    for idx in list(active_strokes.keys()):
        if idx not in present_ids:
            if len(active_strokes[idx]) > 0:
                all_strokes.append(active_strokes[idx])
            active_strokes.pop(idx)

    # Gambar Arsip (Garis Biru)
    for stroke in all_strokes:
        for i in range(1, len(stroke)):
            cv2.line(frame, stroke[i-1], stroke[i], (255, 0, 0), 4)

    # Gambar Coretan Aktif (Garis Kuning)
    for idx, stroke in active_strokes.items():
        for i in range(1, len(stroke)):
            cv2.line(frame, stroke[i-1], stroke[i], (0, 255, 255), 6)

    cv2.imshow("Dual Hand Paint - Fixed", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('c'):
        all_strokes = []
        active_strokes = {}

cap.release()
cv2.destroyAllWindows()