import cv2
import numpy as np

def load_grayscale_image(image_bytes: bytes) -> np.ndarray:
    # Memastikan file tidak kosong
    if not image_bytes:
        raise ValueError("File gambar kosong.")

    # Mengubah bytes menjadi array NumPy
    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    # Membaca gambar dalam grayscale
    gray_image = cv2.imdecode(
        image_array,
        cv2.IMREAD_GRAYSCALE
    )

    # Memastikan gambar berhasil dibaca
    if gray_image is None:
        raise ValueError("Gambar tidak dapat dibaca.")

    return gray_image
