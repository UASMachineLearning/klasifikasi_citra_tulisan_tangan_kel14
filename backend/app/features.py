# features.py
# Ekstraksi 72 fitur GLCM dari area tulisan hasil preprocessing
import numpy as np
from skimage.feature import graycomatrix, graycoprops

# Parameter GLCM
CFG_GLCM = {
    'levels': 32,
    'distances': [1, 3, 5],
    'angles_derajat': [0, 45, 90, 135],
    'properties': [
        'dissimilarity', 'correlation', 'homogeneity',
        'contrast', 'ASM', 'energy'
    ],
    'symmetric': True,
    'normed': True
}

# Membuat nama fitur sesuai urutan ekstraksi
def nama_fitur_glcm():
    return [
        f'{prop}_d{jarak}_a{sudut}'
        for prop in CFG_GLCM['properties']
        for jarak in CFG_GLCM['distances']
        for sudut in CFG_GLCM['angles_derajat']
    ]

# Mengekstraksi fitur tekstur GLCM dari citra grayscale
def ekstraksi_glcm(konten):
    level = CFG_GLCM['levels']
    abu = np.asarray(konten, dtype=np.uint8)

    if abu.ndim != 2:
        raise ValueError('Input GLCM harus berupa citra grayscale.')
    if min(abu.shape) < max(CFG_GLCM['distances']) + 1:
        abu = np.full((8, 8), 255, dtype=np.uint8)

    kuantisasi = (abu.astype(np.uint16) * level // 256).astype(np.uint8)
    sudut = np.deg2rad(CFG_GLCM['angles_derajat'])

    glcm = graycomatrix(
        kuantisasi,
        distances=CFG_GLCM['distances'],
        angles=sudut,
        levels=level,
        symmetric=CFG_GLCM['symmetric'],
        normed=CFG_GLCM['normed']
    )

    fitur = []
    for prop in CFG_GLCM['properties']:
        fitur.extend(graycoprops(glcm, prop).ravel())

    return np.nan_to_num(np.asarray(fitur, dtype=np.float32))
