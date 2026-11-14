from pathlib import Path

import joblib
import numpy as np

from app.preprocessing import load_grayscale_image
from app.features import (
    extract_glcm_features,
    build_feature_dataframe
)

# Menentukan lokasi model SVM
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "model_svm_final.joblib"
)


# Memuat model SVM final
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
        "feature_columns",
        "classes",
        "best_params",
        "glcm_config"
    }

    if not required_keys.issubset(bundle.keys()):
        raise ValueError("Informasi paket model tidak lengkap.")

    if len(bundle["feature_columns"]) != 24:
        raise ValueError("Jumlah fitur model harus 24.")

    return bundle


# Melakukan prediksi identitas penulis
def predict_image(image_bytes: bytes, bundle: dict) -> dict:

    # Membaca gambar dalam grayscale
    gray_image = load_grayscale_image(image_bytes)

    # Mengekstraksi fitur GLCM
    features = extract_glcm_features(
        gray_image,
        bundle["glcm_config"]
    )

    # Menyusun fitur sesuai urutan model
    feature_df = build_feature_dataframe(
        features,
        bundle["feature_columns"]
    )

    # Memastikan jumlah fitur sesuai
    if len(features) != 24:
        raise ValueError("Jumlah fitur GLCM harus 24.")

    # Memastikan seluruh nilai fitur valid
    if not np.isfinite(feature_df.to_numpy()).all():
        raise ValueError("Nilai fitur tidak valid.")

    model = bundle["model"]

    # Memprediksi NIM penulis
    predicted_nim = model.predict(feature_df)[0]

    # Mengambil probabilitas setiap kelas
    probabilities = model.predict_proba(feature_df)[0]

    # Mencari posisi kelas hasil prediksi
    model_classes = np.asarray(model.classes_)

    class_indices = np.flatnonzero(
        model_classes == predicted_nim
    )

    if len(class_indices) != 1:
        raise ValueError("Kelas prediksi tidak ditemukan.")

    # Mengambil confidence sesuai kelas predict()
    class_index = int(class_indices[0])
    confidence = float(probabilities[class_index])

    if not np.isfinite(confidence) or not 0 <= confidence <= 1:
        raise ValueError("Confidence tidak valid.")

    return {
        "predicted_nim": str(predicted_nim),
        "confidence": confidence
    }
