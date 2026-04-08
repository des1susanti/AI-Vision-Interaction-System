import cv2
from ultralytics import YOLO

# 1. Load model Small
model = YOLO('yolov8s.pt')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
last_conf = {}

print("--- AI Visual Feedback System---")
print("User: Desi Susanti")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # 2. Deteksi (Ambang batas 0.3 untuk menangkap objek ragu)
    results = model(frame, stream=True, conf=0.3)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # --- LOGIKA SMOOTHING AGAR ANGKA DIAM ---
            current_conf = float(box.conf[0])
            cls = int(box.cls[0])
            
            if cls in last_conf:
                # Ambil 90% nilai lama + 10% nilai baru agar stabil
                conf = (last_conf[cls] * 0.9) + (current_conf * 0.1)
            else:
                conf = current_conf
            
            last_conf[cls] = conf # Simpan untuk frame berikutnya
            # ----------------------------------------
            
            original_label = model.names[cls].capitalize()
            
            # --- LOGIKA PENYARINGAN & VISUAL FEEDBACK ---
            if conf < 0.55:
                # KONDISI: TIDAK TERDETEKSI (MERAH TEBAL + TANDA SILANG)
                label_name = "X TIDAK TERDETEKSI"
                color = (0, 0, 255) # Merah Terang (BGR)
                is_fixed = False
            else:
                # KONDISI: FIX / YAKIN (HIJAU NEON Tanpa Tanda [V])
                is_fixed = True
                color = (50, 255, 50) # Hijau Neon (Sangat Terang)
                
             # Ambil label dari YOLO dan hitung dimensi
                lbl = original_label.lower()
                w, h = (x2 - x1), (y2 - y1)
                aspect_ratio = h / w if w > 0 else 0

               # Ambil label dari YOLO (pastikan huruf kecil)
                lbl = original_label.lower()
                w = x2 - x1  # lebar objek

                # Koreksi Nama Objek (Versi Stabil)
                if lbl == "person":
                    label_name = "HUMAN"
                
                elif lbl == "cell phone":
                    # Fokus hanya pada ukuran lebar. 
                    # Jika sangat kecil sekali (di bawah 110 pixel), anggap jam tangan.
                    if w < 110:
                        label_name = "SMARTWATCH"
                    else:
                        label_name = "CELL PHONE"

                elif lbl == "bottle":
                    label_name = "TUMBLER"

                elif lbl == "toothbrush":
                    label_name = "PEN"

                # Masukkan Remote & Donut ke Mouse (YOLO sering salah baca mouse jadi 2 benda ini)
                elif lbl in ["remote", "donut", "mouse"]:
                    label_name = "COMPUTER MOUSE"

                elif lbl in ["handbag", "suitcase", "box"]:
                    label_name = "TISSUE / BOX"

                elif lbl in ["sports equipment", "headphones"]:
                    label_name = "HEADSET"

                else:
                    label_name = f"{original_label.upper()}"

            # --- VISUALISASI FRAME (HUD STYLE) ---
            thickness = 3 if not is_fixed else 2
            d = 20 # panjang sudut
            
            # Gambar sudut kotak
            cv2.line(frame, (x1, y1), (x1 + d, y1), color, thickness + 2)
            cv2.line(frame, (x1, y1), (x1, y1 + d), color, thickness + 2)
            cv2.line(frame, (x2, y1), (x2 - d, y1), color, thickness + 2)
            cv2.line(frame, (x2, y1), (x2, y1 + d), color, thickness + 2)
            cv2.line(frame, (x1, y2), (x1 + d, y2), color, thickness + 2)
            cv2.line(frame, (x1, y2), (x1, y2 - d), color, thickness + 2)
            cv2.line(frame, (x2, y2), (x2 - d, y2), color, thickness + 2)
            cv2.line(frame, (x2, y2), (x2, y2 - d), color, thickness + 2)

            # --- TEKS HD HIGH-CONTRAST ---
            display_text = f"{label_name} {int(conf*100)}%"
            font = cv2.FONT_HERSHEY_DUPLEX
            
            # Gambar Background Label (Agar terbaca di background terang/gelap)
            (w_txt, h_txt), _ = cv2.getTextSize(display_text, font, 0.6, 1)
            cv2.rectangle(frame, (x1, y1 - 35), (x1 + w_txt + 10, y1), color, -1)
            
            # Teks Utama (Hitam di atas warna background agar sangat tajam)
            cv2.putText(frame, display_text, (x1 + 5, y1 - 10), 
                        font, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

    # --- HEADER PANEL (DASHBOARD) ---
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (1280, 65), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    cv2.putText(frame, "AI VISION RESEARCH", (30, 42), 
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f"RESEACHER: DESI SUSANTI", (950, 42), 
                cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow("Professional AI Interface", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()