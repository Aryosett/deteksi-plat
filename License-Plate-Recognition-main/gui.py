import streamlit as st
import os
import subprocess
import time

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

# Tombol untuk memulai deteksi
if st.button("Mulai Deteksi", key="start_detection", help="Klik untuk mulai deteksi plat nomor"):
    with st.spinner("Sedang mendeteksi plat nomor..."):
        # Menjalankan main.py menggunakan subprocess
        result = subprocess.run(['python', 'test1.py'], capture_output=True, text=True)
        
        # Menunggu sebentar hingga deteksi selesai
        time.sleep(5)  # Tunggu selama 5 detik sebelum memuat hasil

        # Menampilkan hasil deteksi
        output_folder = "hasil"
        
        # Daftar file dan caption sesuai urutan yang diinginkan
        images = [
            ("result_1_resized.png", "Resize"),
            ("result_1_gray.png", "Konversi ke Grayscale"),
            ("result_1_inverted.png", "Menginvert Gambar"),
            ("result_1_thresh.png", "Tresholding"),
            ("result_1_morph.png", "Transformasi Morph"),
            ("result_1_detected.png", "Hasil")
        ]

        # Menampilkan gambar secara urut
        for file_name, caption in images:
            file_path = os.path.join(output_folder, file_name)
            if os.path.exists(file_path):
                st.image(file_path, caption=caption, use_container_width=True)

        # Menampilkan output dari subprocess jika ada
        if result.stdout:
            # Memastikan hanya "Isi Plat Nomor" yang ditampilkan
            lines = result.stdout.splitlines()
            plat_nomor = ""
            for line in lines:
                if "Isi plat nomor:" in line:
                    plat_nomor = line.split("Isi plat nomor:")[1].strip()  # Menarik isi plat nomor
                    break

            # Menampilkan hanya Isi Plat Nomor jika ditemukan
            if plat_nomor:
                st.write(f"**Isi Plat Nomor**: {plat_nomor}")

        # Jika tidak ada gambar deteksi, beri pesan
        if not any(os.path.exists(os.path.join(output_folder, img[0])) for img in images):
            st.warning("Tidak ada hasil deteksi plat nomor.")
