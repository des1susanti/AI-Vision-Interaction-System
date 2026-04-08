import cv2

# Coba indeks 0, jika tidak muncul coba ganti ke 1
cap = cv2.VideoCapture(0)

print("Menekan 'q' untuk keluar dari kamera...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil gambar. Coba ganti indeks VideoCapture(0) ke 1.")
        break
        
    cv2.imshow('Cek Kamera Mac M4', frame)
    
    # Keluar jika menekan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()