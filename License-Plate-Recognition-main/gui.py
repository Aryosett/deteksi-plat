import streamlit as st
import cv2
import numpy as np
import os

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
st.markdown("<p class='description'>Gunakan aplikasi ini untuk mendeteksi plat nomor kendaraan secara otomatis.<br>NOTE: Ketik S untuk Deteksi dan Q untuk mengakhiri</p>", unsafe_allow_html=True)

# Fungsi untuk menangkap gambar dari kamera
def capture_from_camera():
    # Gunakan st.camera_input untuk menampilkan tampilan kamera
    image = st.camera_input("Ambil Gambar Plat Nomor")
    if image is not None:
        # Konversi gambar ke format OpenCV
        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV
        
        # Tampilkan gambar yang diambil
        st.image(img, channels="BGR", caption="Gambar dari Kamera", use_container_width=True)
        return img
    return None

# Tombol untuk memulai deteksi
if st.button("Mulai Deteksi", key="start_detection", help="Klik untuk mulai deteksi plat nomor"):
    with st.spinner("Sedang mendeteksi plat nomor..."):
        # Ambil gambar dari kamera
        captured_image = capture_from_camera()

        if captured_image is not None:
            # Panggil fungsi deteksi plat nomor di sini, misalnya:
            # result = detect_license_plate(captured_image)
            # Di sini Anda bisa menambahkan proses deteksi plat nomor dengan OpenCV atau TensorFlow sesuai yang Anda miliki
            # Misalnya, jika Anda menggunakan hasil deteksi langsung, tampilkan hasilnya
            st.write("Plat nomor berhasil terdeteksi.")  # Gantilah dengan hasil deteksi Anda
        else:
            st.warning("Tidak ada gambar yang diambil dari kamera.")
