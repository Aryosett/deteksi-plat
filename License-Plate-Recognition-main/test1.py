import cv2
import numpy as np
import pytesseract
import re
import os

# Konfigurasi Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = "c:/Program Files/Tesseract-OCR/tesseract.exe"

# Muat classifier untuk mendeteksi plat nomor
cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

# Buat folder untuk hasil jika belum ada
output_folder = "hasil"
os.makedirs(output_folder, exist_ok=True)

def save_image(image, filename):
    """
    Simpan gambar dengan nama file yang tetap, menggantikan file lama.
    """
    file_path = os.path.join(output_folder, filename)
    cv2.imwrite(file_path, image)
    print(f"Gambar disimpan sebagai '{filename}', menggantikan file lama jika ada.")

def process_plate(plate):
    """
    Preprocessing untuk meningkatkan akurasi OCR pada gambar plat nomor.
    """
    # Resize untuk meningkatkan resolusi
    plate_resized = cv2.resize(plate, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    save_image(plate_resized, "result_1_resized.png")

    # Konversi ke grayscale
    plate_gray = cv2.cvtColor(plate_resized, cv2.COLOR_BGR2GRAY)
    save_image(plate_gray, "result_1_gray.png")

    # Gaussian Blur untuk mengurangi noise
    plate_blurred = cv2.GaussianBlur(plate_gray, (5, 5), 0)

    # Threshold adaptif
    plate_thresh = cv2.adaptiveThreshold(
        plate_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    save_image(plate_thresh, "result_1_thresh.png")

    # Morphological transform untuk menutup celah
    kernel = np.ones((3, 3), np.uint8)
    plate_morph = cv2.morphologyEx(plate_thresh, cv2.MORPH_CLOSE, kernel)
    save_image(plate_morph, "result_1_morph.png")

    return plate_resized, plate_gray, plate_thresh, plate_morph

def extract_text_from_plate(plate_binary):
    """
    Ekstraksi teks dari gambar binary plat nomor menggunakan Tesseract.
    """
    custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(plate_binary, config=custom_config)
    # Filter hasil OCR agar sesuai pola plat nomor
    text = re.sub(r'[^A-Z0-9\s]', '', text)  # Hanya izinkan huruf besar dan angka
    text = ' '.join(text.split())  # Hapus spasi ekstra
    return text

def detect_plate_realtime():
    """
    Deteksi dan baca plat nomor secara real-time menggunakan kamera.
    """
    cap = cv2.VideoCapture(0)  # Membuka kamera

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        nplate = cascade.detectMultiScale(gray, 1.1, 4)
        detected_plate = None  # Menyimpan gambar plat untuk deteksi lebih lanjut
        plate_coords = None

        for (x, y, w, h) in nplate:
            # Tambahkan margin pada plat nomor
            wT, hT, _ = frame.shape
            a, b = (int(0.02 * wT), int(0.02 * hT))
            detected_plate = frame[y+a:y+h-a, x+b:x+w-b, :]
            plate_coords = (x, y, w, h)
            
            # Gambar rectangle pada frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (51, 51, 255), 2)

        # Tampilkan frame kamera
        cv2.imshow("Real-Time License Plate Detection", frame)

        # Kontrol keyboard
        key = cv2.waitKey(1) & 0xFF

        # Jika 's' ditekan, simpan gambar baru dengan nama tetap
        if key == ord('s') and detected_plate is not None:
            # Simpan hasil crop plat nomor
            save_image(detected_plate, "result_1_plate.png")

            # Preprocessing gambar untuk OCR
            plate_resized, plate_gray, plate_thresh, plate_morph = process_plate(detected_plate)

            # OCR untuk membaca teks dari plat nomor
            text = extract_text_from_plate(plate_morph)
            print(f"Isi plat nomor: {text}")

            # Tambahkan hasil deteksi ke frame asli
            if plate_coords:
                x, y, w, h = plate_coords
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Simpan gambar deteksi akhir
            save_image(frame, "result_1_detected.png")

        # Jika 'q' ditekan, keluar dari aplikasi
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Jalankan fungsi
detect_plate_realtime()
