# preprocessing.py
# Dipakai saat training, testing, dan prediksi gambar baru.
import io
import cv2
import numpy as np
from PIL import Image, ImageOps

# Parameter preprocessing
CFG = {
    'sisi_maks': 2400,
    'tinggi_input': 128,
    'lebar_input': 384,
    'background_sigma': 25,
    'margin_min': 8,
    'margin_ratio': 0.01,
    'jarak_baris': 4,
    'skala_maks': 2.0,
}

# Membaca gambar dari path, bytes, PIL, atau array menjadi grayscale
def baca_gambar(sumber):
    if isinstance(sumber, str):
        img = Image.open(sumber)
    elif isinstance(sumber, (bytes, bytearray)):
        img = Image.open(io.BytesIO(sumber))
    elif isinstance(sumber, Image.Image):
        img = sumber
    else:
        arr = np.asarray(sumber)
        if arr.ndim == 3:
            arr = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        img = Image.fromarray(arr)

    img = ImageOps.exif_transpose(img)

    if img.mode in ('RGBA', 'LA') or 'transparency' in img.info:
        img = img.convert('RGBA')
        latar = Image.new('RGBA', img.size, (255, 255, 255, 255))
        latar.alpha_composite(img)
        img = latar

    abu = np.array(img.convert('L'))
    sisi = max(abu.shape)
    if sisi > CFG['sisi_maks']:
        skala = CFG['sisi_maks'] / sisi
        abu = cv2.resize(
            abu, None, fx=skala, fy=skala,
            interpolation=cv2.INTER_AREA
        )
    return abu

# Menormalkan pencahayaan menggunakan estimasi background Gaussian
def koreksi_latar(abu):
    tinggi, lebar = abu.shape
    sigma = min(CFG['background_sigma'], max(2.0, min(tinggi, lebar) / 4))
    latar = cv2.GaussianBlur(abu, (0, 0), sigmaX=sigma, sigmaY=sigma)
    latar = np.maximum(latar, 1)
    hasil = cv2.divide(abu, latar, scale=255)
    return np.clip(hasil, 0, 255).astype(np.uint8)

# Membuat mask sementara untuk mendeteksi area tinta
def deteksi_tinta(abu):
    _, mask = cv2.threshold(
        abu, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    return mask

# Mengambil kotak area tulisan dengan margin adaptif
def crop_adaptif(abu, mask):
    tinggi, lebar = abu.shape
    titik = cv2.findNonZero(mask)

    if titik is None:
        kotak = (0, tinggi, 0, lebar)
        return abu.copy(), mask.copy(), kotak

    x, y, w, h = cv2.boundingRect(titik)
    margin = max(CFG['margin_min'], int(CFG['margin_ratio'] * min(tinggi, lebar)))
    atas = max(0, y - margin)
    bawah = min(tinggi, y + h + margin)
    kiri = max(0, x - margin)
    kanan = min(lebar, x + w + margin)

    roi = abu[atas:bawah, kiri:kanan]
    mask_roi = mask[atas:bawah, kiri:kanan]
    return roi, mask_roi, (atas, bawah, kiri, kanan)

# Menggabungkan celah kosong yang sangat pendek pada proyeksi baris
def isi_celah(proyeksi, batas):
    aktif = proyeksi > 0
    i = 0

    while i < len(aktif):
        if aktif[i]:
            i += 1
            continue

        awal = i
        while i < len(aktif) and not aktif[i]:
            i += 1
        akhir = i

        # Celah hanya diisi jika berada di antara dua bagian tulisan
        if awal > 0 and akhir < len(aktif) and (akhir - awal) <= batas:
            aktif[awal:akhir] = True

    return aktif

# Mendeteksi baris tulisan dan menyusunnya sesuai urutan baca
def susun_baris(roi, mask):
    tinggi, lebar = roi.shape
    mask_dilasi = cv2.dilate(mask, np.ones((3, 1), np.uint8), iterations=1)
    proyeksi = (mask_dilasi > 0).sum(axis=1)
    aktif = isi_celah(proyeksi, max(1, int(tinggi * 0.002)))

    indeks = np.where(aktif)[0]
    if len(indeks) == 0:
        return roi.copy(), 1

    kelompok = np.split(indeks, np.where(np.diff(indeks) > 1)[0] + 1)
    pita = [[int(g.min()), int(g.max()) + 1] for g in kelompok if len(g) > 0]

    if len(pita) <= 1:
        return roi.copy(), 1

    # Band kecil seperti titik atau aksen digabungkan ke baris terdekat
    tinggi_pita = [b - a for a, b in pita]
    tinggi_maks = max(tinggi_pita)
    utama = [p for p in pita if (p[1] - p[0]) >= max(3, 0.30 * tinggi_maks)]
    kecil = [p for p in pita if p not in utama]

    if len(utama) <= 1:
        return roi.copy(), 1

    for p in kecil:
        tengah = (p[0] + p[1]) / 2
        jarak = [abs(tengah - (q[0] + q[1]) / 2) for q in utama]
        i = int(np.argmin(jarak))
        if jarak[i] <= tinggi_maks:
            utama[i][0] = min(utama[i][0], p[0])
            utama[i][1] = max(utama[i][1], p[1])
        else:
            utama.append(p)

    utama = sorted(utama, key=lambda p: p[0])
    jarak = max(CFG['jarak_baris'], int(0.15 * tinggi_maks))
    potongan = []

    for atas, bawah in utama:
        m = max(2, int(0.04 * (bawah - atas)))
        y1 = max(0, atas - m)
        y2 = min(tinggi, bawah + m)
        potongan.append(roi[y1:y2, :])

    # Mempertahankan lebar dan urutan baris, tanpa memotong kata
    tinggi_total = sum(p.shape[0] for p in potongan) + jarak * (len(potongan) - 1)
    hasil = np.full((tinggi_total, lebar), 255, dtype=np.uint8)
    posisi = 0

    for p in potongan:
        hasil[posisi:posisi + p.shape[0], :p.shape[1]] = p
        posisi += p.shape[0] + jarak

    return hasil, len(potongan)

# Mengubah ukuran gambar dan menambahkan padding putih
def resize_padding(abu):
    h, w = abu.shape
    tinggi = CFG['tinggi_input']
    lebar = CFG['lebar_input']

    skala = min(tinggi / h, lebar / w, CFG['skala_maks'])
    h_baru = max(1, min(tinggi, int(round(h * skala))))
    w_baru = max(1, min(lebar, int(round(w * skala))))

    metode = cv2.INTER_AREA if skala < 1 else cv2.INTER_CUBIC
    konten = cv2.resize(abu, (w_baru, h_baru), interpolation=metode)

    kanvas = np.full((tinggi, lebar), 255, dtype=np.uint8)
    y0 = (tinggi - h_baru) // 2
    x0 = (lebar - w_baru) // 2
    kanvas[y0:y0 + h_baru, x0:x0 + w_baru] = konten
    return konten, kanvas

# Menjalankan seluruh tahapan preprocessing satu gambar
def preprocessing_citra(sumber):
    abu = baca_gambar(sumber)
    terkoreksi = koreksi_latar(abu)
    mask = deteksi_tinta(terkoreksi)
    roi, mask_roi, kotak = crop_adaptif(terkoreksi, mask)
    susun, jumlah_baris = susun_baris(roi, mask_roi)
    konten, kanvas = resize_padding(susun)

    return {
        'abu': abu,
        'terkoreksi': terkoreksi,
        'mask': mask,
        'roi': roi,
        'susun': susun,
        'konten': konten,
        'kanvas': kanvas,
        'kotak': kotak,
        'jumlah_baris': jumlah_baris
    }
