import streamlit as st

st.markdown(
    '<div class="heading">'
        '<div class="subbab-judul">UAS Machine Learning</div>'
        "<h1>Tentang Aplikasi</h1>"
        "<p>Penjelasan singkat tentang aplikasi ini</p>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("### Aplikasi ini untuk apa?")
st.write(
    "Aplikasi ini dibuat untuk mendeteksi tulisan tangan seseorang ketika tulisan mereka diupload dalam bentuk gambar (jpg, jpeg, png) untuk diprediksi kepemilikannya berdasarkan condifence (probability) tertinggi."
)

st.markdown("### Bagaimana caranya?")
st.markdown("""
    - Upload foto tulisanmu dengan ukuran tidak lebih dari 10 MB.
    - Klik tombol "Prediksi penulis".
    - Hasil prediksi akan keluar.
""")

st.page_link("home.py", label="Coba Prediksi Tulisanku")

st.markdown("### Teknologi Yang Digunakan")
st.markdown("""
    - FastAPI (Backend)
    - Streamlit (Frontend)
    - SVM & GLCM (Algoritma dan ekstraksi fitur citra)
""")