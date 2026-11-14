import requests
import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

# Endpoint backend FastAPI
API_URL = "http://127.0.0.1:8000/predict"

# Ambil file csv nya
CSV_PATH = Path(__file__).resolve().parent.parent / "data_mahasiswa.csv"

# Konfigurasi halaman
st.set_page_config(
    page_title="Klasifikasi Data Citra Tulisan Tangan",
    page_icon="✍️",
    layout="wide",
)

# Styling
CSS = """
<style>
/* import font */
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif; 
}

h1, h2, h3, .serif {
    font-family: 'Lora', sans-serif !important;
}

.stApp {
    background: #ffffff;
}

.block-container {
    padding-top: 2.2rem;
    max-width: 1100px; 
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #5E1717;
    box-shadow: 5px 0px 22px rgba(0, 0, 0, 0.55);
}

/* Tombol Open Sidebar */
button[data-testid="stExpandSidebarButton"] {
    background-color: #7D1F1F;
    border-radius: 50%;
    border: 1px solid #FFFFFF;
}

button[data-testid="stExpandSidebarButton"] span {
    color: #FFFFFF;
}

button[data-testid="stExpandSidebarButton"]:hover {
    background-color: #5E1717;
}

/* Tombol Close Sidebar */
[data-testid="stSidebarCollapseButton"] button {
    background-color: #F1C6C6;
    border-radius: 50%;
    visibility: visible;
}

[data-testid="stSidebarCollapseButton"] button:hover {
    background-color: #FAEBEB;
}

/* HEADING */
.heading {
  background: linear-gradient(135deg, #7d1f1f 0%, #7d1f1f 100%);
  border-radius: 24px;
  padding: 2rem 2.2rem;
  margin-bottom: 1.8rem;
}

.heading .subbab-judul {
    color: #FFFFFF;
}

.heading h1 { 
    margin: .35rem 0 .45rem;
    font-size: 2.3rem;
    color: #ffffff;
    padding: 0;
}

.heading p {
    color: #ffffff;
    margin: 0;
    font-size: 1rem;
}

.subbab-judul { 
    font-size: .72rem;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #5A4F43; 
    font-weight: 600;
}

.steps {
    display: flex;
    gap: .6rem;
    flex-wrap: wrap;
    margin-top: 1.2rem;
}

.step {
    background: rgba(251,248,243,.95);
    border-radius: 999px;
    padding: .35rem .9rem;
    font-size: .82rem;
    color: #7D1F1F;
}

.step b {
    color: #7D1F1F;
    margin-right: .35rem;
}

/* Judul panel */
.panel-title {
    font-family: 'Lora', Georgia, serif;
    font-size: 1.25rem;
    color: #FFFFFF;
    margin: 0 0 .7rem;
}

.panel-title-kolom {
    font-family: 'Lora', Georgia, serif;
    font-weight: 600;
    font-size: 1.25rem;
    margin: 0 0 .7rem;
}

.nama-anggota-kelompok {
    color: #ffffff;
    display: flex;
    flex-direction: column;
    gap: .3rem;
}

/* Upload */
[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF;
    border: 2px dashed #7d1f1f;
    border-radius: 18px;
    padding: 1.6rem;
    transition: all .2s ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: #FAEBEB;
}

[data-testid="stFileUploaderDropzone"] button {
    border-radius: 12px;
    border: 1px solid #7d1f1f;
    background: #ffffff;
    color: #000000;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: #F1C6C6;
}

.stFileChip {
    border: 1px solid #7D1F1F;
}

/* Preview gambar pas udh diupload */
[data-testid="stImage"] img {
  border-radius: 18px;
  border: 1px solid #7d1f1f;
  box-shadow: 0 6px 24px rgba(91,72,48,.10);
}

[data-testid="stImageCaption"] {
    color: #8A7F72;
}

/* Tombol */
.stButton > button {
    border-radius: 14px;
    padding: .7rem 1rem; font-weight: 600;
    border: 1px solid #8B6F4E;
    transition: all .2s ease;
}

.stButton > button[kind="primary"] {
    background: #7d1f1f;
    color: #FFFFFF;
}

.stButton > button[kind="primary"]:hover {
    background: #FFFFFF;
    color: #7d1f1f;
    border-color: #521212;
}

/* Hasil */
.result-card {
  background: #ffffff;
  border: 1px solid #7D1F1F;
  border-radius: 22px;
  padding: 1.5rem;
  display: flex;
  gap: 1.1rem;
  align-items: center;
  box-shadow: 0 6px 24px rgba(91,72,48,.08);
}

.avatar {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  flex-shrink: 0;
  background: #7d1f1f;
  color: #FBF8F3;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Lora', sans-serif;
  font-size: 1.9rem;
}

.result-name {
    font-family: 'Lora', sans-serif;
    font-size: 2rem;
    color: #3B342C;
    line-height: 1.1;
}

.badge {
    display: inline-block;
    margin-top: .45rem;
    background: #E4EBDD;
    color: #4F6247;
    border-radius: 999px;
    padding: .22rem .75rem;
    font-size: .78rem;
    font-weight: 600;
}

.bars {
    background: #FFFFFF;
    border: 1px solid #7D1F1F;
    border-radius: 22px;
    padding: 1.3rem 1.5rem .5rem;
    margin-top: 1rem;
}

.bar-row {
    margin-bottom: .95rem;
}

.bar-label {
    display: flex;
    justify-content: space-between;
    font-size: .88rem;
    color: #5A4F43;
    margin-bottom: .3rem;
}

.bar-track {
    height: 10px;
    background: #FAEBEB;
    border-radius: 999px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: #F1C6C6;
    border-radius: 999px;
}

.bar-fill.top {
    background: linear-gradient(90deg, #F1C6C6, #E8A1A1);
}

.placeholder {
    background: #FFFFFF;
    border: 2px dashed #7D1F1F;
    border-radius: 22px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    padding: 3.2rem 1.5rem;
    text-align: center;
    color: #8A7F72;
}

.placeholder .icon {
    font-size: 2.3rem;
    margin-bottom: .4rem;
}

.note {
    color: #8A7F72;
    font-size: .8rem;
    margin-top: .9rem;
}
</style>
"""

# Mengizinkan penggunaan css
st.markdown(CSS, unsafe_allow_html=True)

NAMA = pd.read_csv(CSV_PATH, dtype=str).set_index("NIM")["name"].to_dict()

def predict(file_bytes: bytes, filename: str, mime: str):
    """Kirim gambar ke backend, kembalikan list (Nama, probabilitas) terurut dari tertinggi."""
    files = {"file": (filename, file_bytes, mime)}
    response = requests.post(API_URL, files=files, timeout=60)
    response.raise_for_status()
    data = response.json()

    # Hasil setelah prediksi
    results = [(NAMA.get(nim, nim), prob) for nim, prob in data["probabilities"].items()]
    return sorted(results, key=lambda x: x[1], reverse=True)[:5]

# Komponen tampilan hasil prediksi
def render_result(results):
    top_nim, top_prob = results[0]
    st.markdown(
        '<div class="result-card">'
        f'<div class="avatar">{top_nim[0].upper()}</div>'
        "<div>"
            '<div class="subbab-judul">Pemilik Tulisan</div>'
            f'<div class="result-name">{top_nim}</div>'
            f'<span class="badge">Probability {top_prob * 100:.1f}%</span>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    rows = []
    for i, (nim, prob) in enumerate(results):
        fill = "bar-fill top" if i == 0 else "bar-fill"
        rows.append(
            '<div class="bar-row">'
                '<div class="bar-label">'
                    f'<span>{nim}</span>'
                    f'<span>{prob * 100:.1f}%</span>'
                '</div>'
                '<div class="bar-track">'
                    f'<div class="{fill}" style="width:{prob * 100:.1f}%"></div>'
                '</div>'
            "</div>"
        )

    st.markdown(
        '<div class="bars">'
            '<div class="subbab-judul" style="margin-bottom:.9rem">Probabilitas tertinggi</div>'
            + "".join(rows)
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="note">Hasil prediksi berdasarkan model SVM dengan fitur GLCM.</div>',
        unsafe_allow_html=True,
    )

def render_placeholder():
    st.markdown(
        '<div class="placeholder">'
            '<div class="icon">🪶</div>'
                "Hasil prediksi akan muncul di sini<br>setelah Anda mengunggah gambar dan menekan Prediksi."
        "</div>",
        unsafe_allow_html=True,
    )


# SIDEBAR
with st.sidebar:
    st.markdown('<div class="panel-title">Anggota Kelompok 14</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="nama-anggota-kelompok">'
            "<div>- Charly</div>"
            "<div>- Diandra Febry Wijaya</div>"
            "<div>- Monica Irene</div>"
        '</div>',
    unsafe_allow_html=True,
    )
    st.divider()
    st.caption(
        '<div class="nama-anggota-kelompok">'
            "~ Kelompok 14"
        '</div>',
        unsafe_allow_html=True,
    )

# HEADING 
st.markdown(
    '<div class="heading">'
        '<div class="subbab-judul">UAS Machine Learning</div>'
            "<h1>Klasifikasi Data Citra Tulisan Tangan</h1>"
            "<p>Upload foto tulisan tanganmu, dan model akan memprediksi siapa pemiliknya</p>"
            
            '<div class="steps">'
                '<span class="step"><b>1</b>Upload gambar</span>'
                '<span class="step"><b>2</b>Klik tombol prediksi</span>'
                '<span class="step"><b>3</b>Lihat hasilnya</span>'
        "</div>"
    "</div>",
    unsafe_allow_html=True,
)

# Bikin section kolom 1 dan 2
left, right = st.columns(2, gap="large")

# Inisialisasi variabel untuk menyimpan file
file_key = None

with left:
    st.markdown('<div class="panel-title-kolom">Upload tulisan tanganmu</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # simpen nama file & size nya ke file_key
        file_key = f"{uploaded_file.name}-{uploaded_file.size}"

        st.image(
            image,
            # tampilin nama file & size nya brp pixel begitu gambar diupload
            caption=f"{uploaded_file.name} · {image.width} x {image.height} px",
            use_container_width=True,
        )

        if st.button("Prediksi penulis", type="primary", use_container_width=True):
            # loading
            with st.spinner("Model sedang menganalisis tulisan..."):
                try:
                    hasil = predict(
                        uploaded_file.getvalue(),
                        uploaded_file.name,
                        uploaded_file.type,
                    )
                    st.session_state["result"] = (file_key, hasil)
                except requests.exceptions.ConnectionError:
                    st.error("Backend tidak bisa dihubungi. Pastikan uvicorn sedang berjalan.")
                except requests.exceptions.HTTPError as e:
                    st.error(f"Backend mengembalikan error {e.response.status_code}: {e.response.text}")
                except requests.exceptions.Timeout:
                    st.error("Backend terlalu lama merespons. Coba lagi.")

# untuk kolom "right"
with right:
    st.markdown('<div class="panel-title-kolom">Hasil prediksi</div>', unsafe_allow_html=True)
    saved = st.session_state.get("result")
    if saved and saved[0] == file_key:
        render_result(saved[1])
    else:
        render_placeholder()