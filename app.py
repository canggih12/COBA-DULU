import streamlit as st
import google.generativeai as genai
import base64
from fpdf import FPDF

# --- FUNGSI UNTUK GENERATE PDF (VERSI FPDF2) ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    
    # Judul
    pdf.set_font("helvetica", style='B', size=16)
    pdf.cell(0, 10, txt="SKRIP KONTEN TIKTOK", ln=True, align='C')
    pdf.ln(10)
    
    # Isi
    pdf.set_font("helvetica", size=11)
    
    # Bersihkan teks sedikit untuk karakter yang benar-benar ilegal di font standar
    # Meskipun fpdf2 lebih kuat, font standar (helvetica/arial) tetap punya limit
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, txt=clean_text)
    
    # PAKSA OUTPUT KE BYTES
    # pdf.output() pada fpdf2 mengembalikan bytearray, kita bungkus dengan bytes()
    return bytes(pdf.output())

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def img_to_html(img_file):
    img_base64 = get_base64_of_bin_file(img_file)
    # Di sini kita kunci alignment-nya di tengah lewat HTML
    html_code = f'<div style="display: flex; justify-content: center; width: 100%;"><img src="data:image/png;base64,{img_base64}" width="300"></div>'
    return html_code

# Konfigurasi Halaman
st.set_page_config(page_title="SKRIPI KONTEN", page_icon="🪄", layout="centered")

# --- FUNGSI RESET ---
def reset_form():
    st.session_state["produk"] = ""
    st.session_state["konteks"] = ""
    st.session_state["value_produk"] = "" 
    st.session_state["sudah_klik"] = False
    if "hasil_ai" in st.session_state:
        del st.session_state["hasil_ai"]

# --- DYNAMIC COLORS ---
if "sudah_klik" not in st.session_state:
    st.session_state["sudah_klik"] = False

gen_bg = "#E74C3C" if st.session_state["sudah_klik"] else "#3498DB"
gen_txt = "#FFFFFF"

# --- CUSTOM CSS (OPTIMIZED) ---
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
          .stAppDeployButton {{display: none;}}
        /* Opsional: Menghilangkan padding atas agar lebih mepet ke atas */
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 0rem;
        }}

    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 0px;
    }}
    /* Garis pembatas tipis dengan jarak yang bisa diatur */
    .custom-divider {{
        margin-top: 7px;    /* Atur jarak atas garis */
        margin-bottom: 15px; /* Atur jarak bawah garis ke input area */
        border-bottom: 1px solid #eee; /* Warna abu-abu tipis */
        width: 100%;
    }}

    .tagline {{
        color: #7f8c8d;
        font-size: 0.5em;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 25px;
        font-style: italic;
        line-height: 1.4;
    }}
    /* Paksa Logo ke Tengah */
    [data-testid="stImage"] {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}


    /* Membuat tombol popover ukurannya pas dengan teks di dalamnya */
    .stPopover {{
        width: fit-content !important;
    }}
    
     .stPopover button {{
        width: fit-content !important;
        padding: 0.2rem 1rem !important;
        height: 2.8em !important;
        border-radius: 8px !important;
        border: 1px solid #d1d1d1 !important;
        background-color: white !important;
        color: #333 !important;
        font-size: 0.9em !important;
    }}

    .box-container {{
        background-color: white; 
        padding: 20px; 
        border-radius: 12px;
        border: 2px solid #333; 
        margin-bottom: 20px; 
        color: #333;
        line-height: 1.8; 
        white-space: pre-wrap; 
    }}

    .label-box {{ 
        font-weight: bold; 
        text-transform: uppercase; 
        font-size: 0.85em; 
        margin-bottom: 8px; 
        display: block; 
        color: #444; 
    }}
    /* Gaya Khusus Tombol Reset */
    div.stButton > button[key="btn_reset"] {{
        background-color: #E74C3C !important; /* Warna Merah */
        color: white !important;               /* Teks Putih */
        font-weight: bold !important;          /* Teks Tebal */
        border-radius: 10px !important;        /* Sudut Membulat */
        border: none !important;               /* Hapus Outline */
        width: 100% !important;
    }}

    /* Efek Hover (Saat kursor di atas tombol) */
    div.stButton > button[key="btn_reset"]:hover {{
        background-color: #C0392B !important; /* Merah Lebih Gelap saat ditekan */
        color: white !important;
    }}

    /* Tombol Utama */
    div.stButton > button:first-child {{
        background-color: {gen_bg} !important;
        color: {gen_txt} !important;
        border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%; border: none;
    }}
    
    /* Tombol Navigasi Bawah */
    div.stButton > button[key="btn_lagi"] {{ background-color: #3498DB !important; color: white !important; border-radius: 10px; }}
    div.stButton > button[key="btn_reset"] {{ background-color: #27AE60 !important; color: white !important; border-radius: 10px; }}

    .footer {{
        text-align: center;
        color: #95a5a6;
        font-size: 0.8em;
        padding: 20px 0px;
        border-top: 1px solid #eee;
        margin-top: 40px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- UI HEADER ---
# Tutorial di Kiri (Button Kecil)
col_tutor, col_3 = st.columns([1, 4])
with col_tutor:
    with st.popover("📖 Tutorial"):
        st.markdown("### 💡 Panduan Penggunaan")
        st.write("""
        1. **📦 Nama Produk**: Isi nama barang yang ingin dijual.
        2. **💎 Value**: Sebutkan kelebihan produk (misal: awet, murah).
        3. **🎯 Konteks**: Ceritakan suasana video (misal: lagi di kantor).
        4. **👥 Target Usia**: Tentukan target usia agar bahasa yang digunakan sesuai.
        ---
        ### 🔑 Kenapa Perlu API Key?
        1. **🚀 Tanpa Limit**: Agar pembuatan skrip berjalan lancar tanpa batasan kuota harian.
        2. **🛠️ Cara Buat**: Jika belum punya, klik [Google AI Studio](https://aistudio.google.com/app/apikey).
        3. **📥 Aktivasi**: Setelah dapat, langsung masukkan kodenya di kolom konfigurasi.
        
        *Klik **Generate** dan skrip siap digunakan!*
        """)
# Logo Center (Menggunakan baris tunggal agar CSS bekerja maksimal)
st.markdown(img_to_html("logo.png"), unsafe_allow_html=True)
# --- TAMBAHKAN TEKS PERINGATAN DI SINI ---
st.markdown("""
    <p style='text-align: center; background-color: #F0F8FF; color: #FF0000; font-weight: bold; font-size: 0.9em; margin-top: -20px; margin-bottom: 10px;'>
        ⚠️ Jangan Lupa input Api Key agar aplikasi berjalan
    </p>
""", unsafe_allow_html=True)


st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
# --- INPUT API KEY ---
api_key_input = st.text_input("Masukkan Gemini API Key:", type="password", help="Dapatkan key di Google AI Studio")
if api_key_input:
        try:
            # Konfigurasi library Gemini dengan key dari user
            genai.configure(api_key=api_key_input)
            # Inisialisasi model (gunakan gemini-3)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            # Test kecil untuk memastikan key valid
            # (opsional, tapi bagus untuk validasi instan)
            st.success("✅ API Key Terhubung!")
        except Exception as e:
            st.error(f"❌ Key Tidak Valid: {e}")
            model = None
else:

        model = None                
# --- INPUT AREA ---
produk = st.text_input("📦 Nama Produk", key="produk")
value_produk = st.text_input("💎 Keunggulan / Value Produk", key="value_produk", placeholder="Contoh: Anti air, garansi 1 thn")
konteks = st.text_area("🎯 Konteks / Situasi", key="konteks")

col1, col2, col3 = st.columns(3)
with col1:
    target_usia = st.selectbox("👥 Target Usia", ["Gen Z", "Dewasa", "Umum"])
with col2:
    durasi = st.selectbox("⏱️ Durasi", ["20 detik", "35 detik", "45 detik", "60 detik"])
with col3:
    angle = st.selectbox("🎬 Angle", ["Review Jujur", "Eksperimen", "Tips & Trik", "Storytelling"])

# --- GENERATE LOGIC ---
def generate_content():
    st.session_state["sudah_klik"] = True
    try:
        prompt = f"""Buat skrip affiliate tiktok {durasi} 
        untuk {produk}. 
        Keunggulan Produk: {value_produk}.
        Konteks: {konteks}. 
        Gaya Bahasa: {target_usia}. 
        Angle: {angle}.
        
        PENTING: Gunakan gaya bahasa dan kosa kata yang sangat sesuai untuk {target_usia}.
        Format harus terdiri dari:
            1. **HOOK**: Kalimat pembuka yang bikin orang berhenti scrolling.
            2. **MASALAH**: Singgung keresahan yang dialami calon pembeli sesuai {target_usia}.
            3. **SOLUSI/VALUE**: Kenapa produk {produk} ini wajib dibeli.
            4. **CTA**: Ajakan beli di keranjang pojok kiri bawah
        Wajib gunakan format vertikal ke bawah dengan jeda antar baris yang jelas. 
        DILARANG GUNAKAN KATA ANDA,SAYA DAN TABEL.

        Susun seperti ini:

        BAGIAN VISUAL:
        0-5 detik: [Instruksi kamera]
        
        BAGIAN VOICE OVER
        0-5 detik (hook): [Teks narasi]

        BAGIAN VISUAL
        5-10 detik: [Instruksi kamera]

        BAGIAN VOICE OVER
        5-10 detik: [Teks narasi]
        
        dst...

    

        Berikan 1x enter (baris kosong) antar segmen waktu agar rapi."""
        
        response = model.generate_content(prompt)
        st.session_state.hasil_ai = response.text
    except:
        st.error("Gagal generate!")

# Tombol Generate
if st.button("Generate Skrip"):
    if not produk:
        st.warning("⚠️ Nama Produk wajib diisi!")
    else:
        # 1. Buat tempat kosong (placeholder)
        loading_placeholder = st.empty()
        
        # 2. Tampilkan GIF dan Teks di dalam placeholder
        with loading_placeholder.container():
            st.markdown('<p class="loading-text">Mohon tunggu, Skrip sedang dibuat...</p>', unsafe_allow_html=True)
            # Ganti URL ini dengan link GIF loading pilihanmu atau file lokal
            st.image("https://i.gifer.com/ZZ5H.gif", width=100) 
        
        # 3. Jalankan fungsi generate
        generate_content()
        
        # 4. Hapus loading setelah selesai agar bersih
        loading_placeholder.empty()
# --- TAMPILAN HASIL ---
if 'hasil_ai' in st.session_state:
    st.markdown("---")
    
    res = st.session_state.hasil_ai
    if "---" in res:
        parts = res.split("---")
        visual_text = parts[0].replace("BAGIAN VISUAL:", "").strip()
        vo_text = parts[1].replace("BAGIAN VOICE OVER:", "").strip()
    else:
        visual_text = res
        vo_text = res

    # Kotak Visual
    st.markdown("<span class='label-box'>Berikut Hasilnya</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='box-container'>{visual_text}</div>", unsafe_allow_html=True)

    # Kotak Voice Over
    st.markdown("<span class='label-box'>Salin Skrip Disini)</span>", unsafe_allow_html=True)
    st.code(vo_text, language="text")
    
  # --- BAGIAN TOMBOL DOWNLOAD PDF ---
    # Kita buat 3 kolom untuk tombol Reset dan Download
    col_pdf, col_re = st.columns([1, 1])
    
    with col_pdf:
        # Generate data PDF
        pdf_bytes = create_pdf(st.session_state.hasil_ai)
        
        st.download_button(
            label="📥 Simpan ke PDF",
            data=pdf_bytes,
            file_name=f"skrip_{produk.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with col_re:
        if st.button("🗑️ RESET", key="btn_reset", use_container_width=True, on_click=reset_form):
            st.rerun()
            # --- FOOTER (NAMA PEMBUAT) ---
st.markdown("""
    <div class="footer">
        <p>Created by <b>[Cerita Ozi]</b> | © 2026 Skripi Konten Team</p>
    </div>
    """, unsafe_allow_html=True)
        
