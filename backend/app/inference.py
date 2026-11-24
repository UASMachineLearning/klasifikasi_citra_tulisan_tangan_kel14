from pathlib import Path

import joblib
import numpy as np

from app.preprocessing import preprocessing_citra
from app.features import ekstraksi_glcm, nama_fitur_glcm

# Menentukan lokasi model SVM final
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "model_svm_final.joblib"
)


# Memuat model SVM final dan memeriksa kesesuaian konfigurasi

def load_model_bundle() -> dict:

    # Memastikan file model tersedia
    if not MODEL_PATH.is_file():
        raise FileNotFoundError("Model SVM tidak ditemukan.")

    # Memuat paket model
    bundle = joblib.load(MODEL_PATH)

    if not isinstance(bundle, dict):
        raise ValueError("Format paket model tidak valid.")

    # Memastikan informasi model tersedia
    required_keys = {
        "model",
        "kelas",
        "feature_names"
    }

    if not required_keys.issubset(bundle.keys()):
        raise ValueError("Informasi paket model tidak lengkap.")

    model = bundle["model"]
    kelas = np.asarray(bundle["kelas"]).astype(str)
    feature_names = list(bundle["feature_names"])

    # Memastikan jumlah kelas dan fitur sesuai model hasil notebook
    if len(kelas) != 50:
        raise ValueError("Model harus memiliki 50 kelas penulis.")

    if len(feature_names) != 72:
        raise ValueError("Model harus menggunakan 72 fitur GLCM.")

    # Memastikan urutan fitur sama dengan proses ekstraksi pada notebook
    if feature_names != nama_fitur_glcm():
        raise ValueError("Urutan fitur GLCM tidak sesuai dengan model.")

    # Memastikan urutan indeks kelas sesuai dengan mapping NIM
    model_classes = np.asarray(model.classes_, dtype=int)
    expected_classes = np.arange(len(kelas))

    if not np.array_equal(model_classes, expected_classes):
        raise ValueError("Mapping kelas model tidak sesuai dengan daftar NIM.")

    if getattr(model, "n_features_in_", None) != len(feature_names):
        raise ValueError("Jumlah fitur input model tidak sesuai.")

    bundle["kelas"] = kelas
    bundle["feature_names"] = feature_names

    return bundle


# Melakukan prediksi identitas penulis

def predict_image(image_bytes: bytes, bundle: dict) -> dict:

    # Memastikan file gambar tidak kosong
    if not image_bytes:
        raise ValueError("File gambar kosong.")

    # Menjalankan preprocessing yang sama dengan notebook
    hasil = preprocessing_citra(image_bytes)

    # Mengekstraksi 72 fitur GLCM dari area tulisan
    features = ekstraksi_glcm(hasil["konten"])

    # Memastikan jumlah fitur sesuai model
    if len(features) != len(bundle["feature_names"]):
        raise ValueError("Jumlah fitur GLCM tidak sesuai dengan model.")

    # Memastikan seluruh nilai fitur valid
    if not np.isfinite(features).all():
        raise ValueError("Nilai fitur GLCM tidak valid.")

    # Menyiapkan fitur sebagai input model
    feature_input = features.reshape(1, -1)
    model = bundle["model"]
    kelas = bundle["kelas"]

    # Memprediksi indeks kelas penulis
    predicted_index = int(model.predict(feature_input)[0])

    # Mengambil probabilitas seluruh kelas
    probability_row = model.predict_proba(feature_input)[0]
    model_classes = np.asarray(model.classes_, dtype=int)

    if len(probability_row) != len(model_classes):
        raise ValueError("Jumlah probabilitas tidak sesuai dengan kelas model.")

    if predicted_index < 0 or predicted_index >= len(kelas):
        raise ValueError("Indeks kelas hasil prediksi tidak valid.")

    # Menerjemahkan indeks kelas menjadi NIM
    predicted_nim = str(kelas[predicted_index])

    # Mengambil confidence sesuai kelas hasil prediksi
    posisi = np.flatnonzero(model_classes == predicted_index)

    if len(posisi) != 1:
        raise ValueError("Kelas prediksi tidak ditemukan pada model.")

    confidence = float(probability_row[int(posisi[0])])

    if not np.isfinite(confidence) or not 0 <= confidence <= 1:
        raise ValueError("Confidence tidak valid.")

    # Menyusun probabilitas seluruh kelas dengan label NIM
    confidence_row = {
        str(kelas[int(class_index)]): float(probability)
        for class_index, probability in zip(model_classes, probability_row)
    }

    return {
        "predicted_nim": predicted_nim,
        "confidence": confidence,
        "confidence_row": confidence_row
    }
