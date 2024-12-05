import streamlit as st
import os
import subprocess
import time
import cv2
import numpy as np
import pytesseract
import re

# Pengaturan Layout dan Tampilan Aplikasi
st.set_page_config(page_title="Aplikasi Deteksi Plat Nomor", page_icon=":car:", layout="centered")

# Menambahkan gaya CSS untuk meningkatkan tampilan
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 40px;
            color: #4CAF50;
            font-weight: bold;
        }
        .description {
            text-align: center;
            font-size: 20px;
            color: #555;
            margin-bottom: 30px;
        }
        .button {
            display: block;
            margin: 0 auto;
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 15px 30px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: #45a049;
        }
        .stImage {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Header dan Deskripsi Aplikasi
st.markdown("<h1 class='title'>Aplikasi Deteksi Plat Nomor</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Gunakan aplikasi ini untuk mendeteksi plat nomor kendaraan secara otomatis.<br>NOTE: Ambil gambar dengan kamera dan klik 'Deteksi'</p>", unsafe_allow_html=True)

# Fungsi deteksi plat nomor
def detect_plate_from_image(image):
    # Konfigurasi Tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = "c:/Program Files/Tesseract-OCR/tesseract.exe"

    # Muat classifier untuk mendeteksi plat nomor
    cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

    # Konversi gambar menjadi array NumPy
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    nplate = cascade.detectMultiScale(gray, 1.1, 4)
    detected_plate = None  # Menyimpan gambar plat untuk deteksi lebih lanjut
    plate_coords = None

    for (x, y, w, h) in nplate:
        # Tambahkan margin pada plat nomor
        wT, hT, _ = image_np.shape
        a, b = (int(0.02 * wT), int(0.02 * hT))
        detected_plate = image_np[y + a:y + h - a, x + b:x + w - b, :]
        plate_coords = (x, y, w, h)

        # Gambar rectangle pada frame
        cv2.rectangle(image_np, (x, y), (x + w, y + h), (51, 51, 255), 2)

    return detected_plate, image_np, plate_coords

# Fungsi untuk mengekstraksi teks dari plat nomor
def extract_text_from_plate(plate_binary):
    custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(plate_binary, config=custom_config)
    text = re.sub(r'[^A-Z0-9\s]', '', text)  # Hanya izinkan huruf besar dan angka
    text = ' '.join(text.split())  # Hapus spasi ekstra
    return text

# Menangkap input gambar dari kamera
image_file = st.camera_input("Ambil Gambar Plat Nomor")

if image_file is not None:
    st.image(image_file, caption="Gambar yang Diambil", use_container_width=True)

    # Ketika tombol "Deteksi" ditekan
    if st.button("Deteksi Plat Nomor"):
        with st.spinner("Sedang mendeteksi plat nomor..."):
            # Deteksi plat nomor dari gambar
            detected_plate, frame_with_detection, plate_coords = detect_plate_from_image(image_file)

            if detected_plate is not None:
                # Proses gambar plat nomor (resize, grayscale, threshold, dll.)
                plate_resized = cv2.resize(detected_plate, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
                plate_gray = cv2.cvtColor(plate_resized, cv2.COLOR_BGR2GRAY)
                plate_blurred = cv2.GaussianBlur(plate_gray, (5, 5), 0)
                plate_thresh = cv2.adaptiveThreshold(plate_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                plate_morph = cv2.morphologyEx(plate_thresh, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

                # Ekstraksi teks
                text = extract_text_from_plate(plate_morph)

                # Menampilkan hasil deteksi
                st.image(frame_with_detection, caption="Hasil Deteksi Plat Nomor", use_container_width=True)
                st.write(f"**Isi Plat Nomor**: {text}")
            else:
                st.warning("Plat nomor tidak terdeteksi!")
