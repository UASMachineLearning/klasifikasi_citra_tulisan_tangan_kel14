# Aplikasi Klasifikasi Data Citra Tulisan Tangan

## Tentang Aplikasi

Aplikasi streamlit ini dikembangkan untuk mengidentifikasi penulis berdasarkan karakteristik visual citra tulisan tangan secara sederhana. Pengguna dapat mengunggah gambar tulisan tangan, kemudian sistem akan memproses gambar dan memprediksi identitas penulis berupa NIM beserta tingkat confidence hasil prediksi. Aplikasi menggunakan model Machine Learning SVM dengan ekstraksi fitur GLCM.

## Anggota Kelompok A14
- Charly (535250039)
- Diandra Febry Wijaya (535250040)
- Monica Irene (535250041)

## Cara Menjalankan Aplikasi

**1. Persiapan**

Pastikan Python versi 3.9–3.13 sudah terpasang.

Periksa versi Python yang tersedia:

```powershell
py --list
```

**2. Buat virtual environment**

Sesuaikan versi Python dengan yang tersedia di komputer masing-masing. Contoh menggunakan Python 3.12:

```powershell
py -3.12 -m venv backend\.venv
```

**3. Install dependencies**

```powershell
.\backend\.venv\Scripts\python.exe -m pip install --upgrade pip
.\backend\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**4. Jalankan aplikasi**

```powershell
.\run.bat
```

**5. Buka aplikasi**

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Dokumentasi API: http://localhost:8000/docs

Pastikan backend dan frontend berjalan selama aplikasi digunakan.
