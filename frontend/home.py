import requests
import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

# Endpoint backend FastAPI
API_URL = "http://127.0.0.1:8000/predict"

# Ambil file csv nya
CSV_PATH = Path(__file__).resolve().parent.parent / "data_mahasiswa.csv"

NAMA = pd.read_csv(CSV_PATH, dtype=str).set_index("NIM")["name"].to_dict()

def predict(file_bytes: bytes, filename: str, mime: str):
    files = {"file": (filename, file_bytes, mime)}
    response = requests.post(API_URL, files=files, timeout=60)
    response.raise_for_status()
    data = response.json()

    # Hasil setelah prediksi
    results = [(nim, NAMA.get(nim, nim), prob) for nim, prob in data["confidence_row"].items()]
    return sorted(results, key=lambda x: x[2], reverse=True)[:5]

# Komponen tampilan hasil prediksi
def render_result(results):
    top_nim, top_name, top_prob = results[0]
    st.markdown(
        '<div class="result-card">'
        f'<div class="avatar">{top_name[0].upper()}</div>'
        "<div>"
            '<div class="subbab-judul">Pemilik Tulisan</div>'
            f'<div class="result-name">{top_name} - {top_nim}</div>'
            f'<span class="badge">Probability {top_prob * 100:.1f}%</span>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # menyimpan hasil untuk urutan confidence
    rows = []

    # loop untuk menampilkan persentase confidence 
    for i, (nim, name, prob) in enumerate(results):
        # bar dengan probability tertinggi
        fill = "bar-fill top" if i == 0 else "bar-fill"
        rows.append(
            '<div class="bar-row">'
                '<div class="bar-label">'
                    f'<span>{name} - {nim}</span>'
                    # persentase
                    f'<span>{prob * 100:.1f}%</span>'
                '</div>'
                '<div class="bar-track">'
                    # persentase bar nya 
                    f'<div class="{fill}" style="width:{prob * 100:.1f}%"></div>'
                '</div>'
            "</div>"
        )

    st.markdown(
        '<div class="bars">'
            '<div class="subbab-judul" style="margin-bottom:.9rem">Tingkat Keyakinan Model</div>'
            + "".join(rows)
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="note">Hasil prediksi berdasarkan model SVM dengan fitur GLCM.</div>',
        unsafe_allow_html=True,
    )



# Fungsi grafik 
def render_confidence_chart(results):

    # Membuat DataFrame untuk grafik
    df_chart = pd.DataFrame({
        "Nama": [name for nim, name, prob in results],
        "NIM": [nim for nim, name, prob in results],
        "Confidence": [float(prob) for nim, name, prob in results]
    })

    # Menggabungkan nama dan NIM 
    df_chart["Label"] = df_chart["Nama"] + "|" + df_chart["NIM"]

    # Container grafik
    with st.container(key="confidence_chart"):

        st.markdown(
            '<div class="chart-title">Grafik Tingkat Keyakinan Model</div>',
            unsafe_allow_html=True,
        )

        chart_spec = {
            "mark": {
                "type": "bar",
                "color": "#7D1F1F",
                "cornerRadiusEnd": 6
            },
            "encoding": {
                "x": {
                    "field": "Label",
                    "type": "nominal",
                    "sort": {
                        "field": "Confidence",
                        "order": "descending"
                    },
                    "axis": {
                        "title": "Nama Mahasiswa / NIM",
                        "labelExpr": "split(datum.label, '|')",
                        "labelAngle": 0,
                        "labelAlign": "center",
                        "labelLimit": 180,
                        "labelFontSize": 10,
                        "titlePadding": 18
                    }
                },
                "y": {
                    "field": "Confidence",
                    "type": "quantitative",
                    "scale": {
                        "zero": True
                    },
                    "axis": {
                        "title": "Confidence (%)",
                        "tickCount": 5,
                        "titlePadding": 12,
                        "format": ".0%"
                    }
                },
                "tooltip": [
                    {
                        "field": "Nama",
                        "type": "nominal",
                        "title": "Nama Mahasiswa"
                    },
                    {
                        "field": "NIM",
                        "type": "nominal",
                        "title": "NIM"
                    },
                    {
                        "field": "Confidence",
                        "type": "quantitative",
                        "title": "Confidence",
                        "format": ".1%"
                    }
                ]
            },
            "height": 360,
            "autosize": {
                "type": "fit",
                "contains": "padding",
                "resize": True
            },
            "config": {
                "view": {
                    "stroke": "transparent"
                },
                "axis": {
                    "labelFont": "Plus Jakarta Sans",
                    "titleFont": "Plus Jakarta Sans",
                    "labelColor": "#5A4F43",
                    "titleColor": "#7D1F1F",
                    "gridColor": "#F1E5E5",
                    "domainColor": "#D9C5C5",
                    "tickColor": "#D9C5C5",
                    "labelFontSize": 12,
                    "titleFontSize": 13
                }
            }
        }

        # Menampilkan grafik
        st.vega_lite_chart(
            df_chart,
            spec=chart_spec,
            use_container_width=True
        )


def render_placeholder():
    st.markdown(
        '<div class="placeholder">'
            '<div class="icon">🪶</div>'
                "Hasil prediksi akan muncul di sini<br>setelah Anda mengunggah gambar dan menekan Prediksi."
        "</div>",
        unsafe_allow_html=True,
    )

# HEADING 
st.markdown(
    '<div class="heading">'
        '<div class="subbab-judul">UAS Machine Learning</div>'
            "<h1>Klasifikasi Data Citra Tulisan Tangan</h1>"
            "<p>Upload foto tulisan tanganmu, dan model akan memprediksi siapa pemiliknya</p>"
            
            '<div class="steps">'
                '<span class="step">Upload gambar</span>'
                '<span class="step">Klik tombol prediksi</span>'
                '<span class="step">Lihat hasilnya</span>'
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
    st.markdown(
        '<div class="panel-title-kolom">Hasil prediksi</div>',
        unsafe_allow_html=True
    )

    saved = st.session_state.get("result")

    if saved and saved[0] == file_key:
        render_result(saved[1])
    else:
        render_placeholder()


# Nampilin grafik ditengah
if saved and saved[0] == file_key:

    # Membuat kolom kosong di kiri dan kanan
    col_kiri, col_grafik, col_kanan = st.columns([1, 5, 1])

    with col_grafik:
        render_confidence_chart(saved[1])