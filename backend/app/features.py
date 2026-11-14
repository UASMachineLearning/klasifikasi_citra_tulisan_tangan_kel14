import numpy as np
import pandas as pd

from skimage.feature import graycomatrix, graycoprops

# Mengekstraksi fitur GLCM dari gambar grayscale
def extract_glcm_features(
    gray_image: np.ndarray,
    glcm_config: dict
) -> dict:

    # Memastikan gambar berupa grayscale
    if gray_image is None or gray_image.ndim != 2:
        raise ValueError("Gambar harus berupa grayscale.")

    if gray_image.dtype != np.uint8:
        raise ValueError("Tipe data gambar harus uint8.")

    # Mengambil konfigurasi GLCM dari model
    distances = glcm_config["distances"]
    angles = glcm_config["angles"]
    properties = glcm_config["properties"]
    angle_names = glcm_config["nama_sudut"]

    # Memastikan konfigurasi sesuai penelitian
    if len(distances) != 1:
        raise ValueError("Model harus menggunakan satu distance.")

    if len(angles) != len(angle_names):
        raise ValueError("Jumlah sudut tidak sesuai.")

    # Menghitung matriks GLCM
    glcm = graycomatrix(
        gray_image,
        distances=distances,
        angles=angles,
        levels=glcm_config["levels"],
        symmetric=glcm_config["symmetric"],
        normed=glcm_config["normed"]
    )

    features = {}

    # Mengambil nilai setiap properti GLCM
    for property_name in properties:
        values = graycoprops(
            glcm,
            property_name
        )

        # Menyimpan nilai berdasarkan sudut
        for index, angle_name in enumerate(angle_names):
            feature_name = f"{property_name}_{angle_name}"

            features[feature_name] = float(
                values[0, index]
            )

    return features

# Menyusun fitur sesuai urutan model SVM
def build_feature_dataframe(
    features: dict,
    feature_columns: list
) -> pd.DataFrame:

    # Memastikan jumlah fitur sesuai
    if len(features) != len(feature_columns):
        raise ValueError("Jumlah fitur tidak sesuai dengan model.")

    # Memastikan nama fitur sesuai
    if set(features.keys()) != set(feature_columns):
        raise ValueError("Nama fitur tidak sesuai dengan model.")

    # Menyusun nilai fitur sesuai urutan training
    feature_values = [
        features[column]
        for column in feature_columns
    ]

    # Membentuk DataFrame untuk input model
    feature_df = pd.DataFrame(
        [feature_values],
        columns=feature_columns
    )

    return feature_df
