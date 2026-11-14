import streamlit as st

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
.stButton > button,
.stButton > button p {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    border-radius: 14px;
    padding: .7rem 1rem;
    font-weight: 600;
    border: 1px solid #8B6F4E;
    transition: all .2s ease;
}

.stButton > button p {
    border: none;
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

[data-testid="stSidebarNav"] span {
    color: #FFFFFF;
}


[data-testid="stPageLink"] p {
    background: #7d1f1f;
    border: 1px solid #8B6F4E;
    border-radius: 14px;
    padding: .7rem 1rem;
    font-weight: 600;
    justify-content: center;
    transition: .2s ease;
    color: #FFFFFF;
}

[data-testid="stPageLink"] p:hover {
    background: #FFFFFF;
    border-color: #521212;
    color: #7d1f1f !important;
}

[data-testid="stPageLink"] a:hover {
    background: transparent;
}

</style>
"""

# Mengizinkan penggunaan css
st.markdown(CSS, unsafe_allow_html=True)

# Daftar halaman
home = st.Page("home.py", title="Home", default=True)
about = st.Page("about.py", title="About Our App")

# Navbar 
pg = st.navigation([home, about], position="top")

# Sidebar
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

pg.run()