from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.inference import load_model_bundle, predict_image

# Membuat aplikasi FastAPI
app = FastAPI(
    title="Handwriting Identifier API",
    description="API untuk mengidentifikasi penulis berdasarkan gambar tulisan tangan.",
    version="1.0.0"
)

# Memuat model ketika backend mulai berjalan
model_bundle = load_model_bundle()

# Endpoint untuk memeriksa status backend
@app.get("/")
def home():

    return {
        "message": "Handwriting Identifier API berjalan.",
        "status": "success"
    }

# Endpoint untuk memprediksi penulis
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Memastikan format file didukung
    allowed_extensions = {".jpg", ".jpeg", ".png"}

    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Format file harus JPG, JPEG, atau PNG."
        )

    # Membaca isi file yang diupload
    image_bytes = await file.read()

    # Preprocessing dan prediksi
    try:
        result = predict_image(
            image_bytes,
            model_bundle
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    # Mengembalikan hasil prediksi
    return {
        "predicted_nim": result["predicted_nim"],
        "confidence": result["confidence"]
    }
