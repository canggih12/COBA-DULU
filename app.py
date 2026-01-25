import streamlit as st
import google.generativeai as genai
import base64

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

# --- SETUP API KEY ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3-flash-preview')
except:
    st.error("API Key belum diset di Secrets!")

# --- DYNAMIC COLORS ---
if "sudah_klik" not in st.session_state:
    st.session_state["sudah_klik"] = False

gen_bg = "#E74C3C" if st.session_state["sudah_klik"] else "#3498DB"
gen_txt = "#FFFFFF"

# --- CUSTOM CSS (OPTIMIZED) ---
st.markdown(f"""
    <style>
    /* Menghilangkan margin berlebih di atas */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}
    
    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 0px;
    }}
    /* Garis pembatas tipis dengan jarak yang bisa diatur */
    .custom-divider {{
        margin-top: 5px;    /* Atur jarak atas garis */
        margin-bottom: 20px; /* Atur jarak bawah garis ke input area */
        border-bottom: 1px solid #eee; /* Warna abu-abu tipis */
        width: 100%;
    }}

    .tagline {{
        color: #7f8c8d;
        font-size: 0,5 em;
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

    /* Kecilkan Tombol Tutorial & Geser Kiri */
    .stPopover {{
        text-align: left !important;
        display: inline-block !important;
    }}
    
    .stPopover button {{
        width: auto !important;
        padding: 0px 15px !important;
        height: 2.5em !important;
        font-size: 0.8em !important;
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
col_tutor, col_empty = st.columns([1, 3]) # Kolom kecil di kiri, sisanya kosong
with col_tutor:
    with st.popover("📖 Tutorial"):
        st.markdown("### 💡 Panduan Penggunaan")
        st.write("""
        1. **📦 Nama Produk**: Isi nama barang yang ingin dijual.
        2. **💎 Value**: Sebutkan kelebihan produk (misal: awet, murah).
        3. **🎯 Konteks**: Ceritakan suasana video (misal: lagi di kantor).
        4. **👥 Target Usia**: AI akan menyesuaikan gaya bahasa (Gaul vs Formal).
        5. **🎬 Angle**: Pilih cara penyampaian konten yang kamu mau.
        
        *Klik **Generate** dan skrip siap digunakan!*
        """)
# Logo Center (Menggunakan baris tunggal agar CSS bekerja maksimal)
st.markdown(img_to_html("logo.png"), unsafe_allow_html=True)

# Tagline Center
st.markdown("<p class='tagline'>\"Rancang Skrip Video Viral & Auto-Cuan\"</p>", unsafe_allow_html=True)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
# --- INPUT AREA ---
produk = st.text_input("📦 Nama Produk", key="produk")
value_produk = st.text_input("💎 Keunggulan / Value Produk", key="value_produk", placeholder="Contoh: Anti air, garansi 1 thn")
konteks = st.text_area("🎯 Konteks / Situasi", key="konteks")

col1, col2, col3 = st.columns(3)
with col1:
    target_usia = st.selectbox("👥 Target", ["Gen Z", "Dewasa", "Umum"])
with col2:
    durasi = st.selectbox("⏱️ Durasi", ["30 detik", "60 detik"])
with col3:
    angle = st.selectbox("🎬 Angle", ["Review Jujur", "Storytelling"])

# --- GENERATE LOGIC ---
def generate_content():
    st.session_state["sudah_klik"] = True
    try:
        prompt = f"Buat skrip affiliate {durasi} untuk {produk}. Keunggulan: {value_produk}. Konteks: {konteks}. Target: {target_usia}. Angle: {angle}. Gunakan bahasa sesuai target. Pisahkan BAGIAN VISUAL dan BAGIAN VOICE OVER dengan '---'."
        response = model.generate_content(prompt)
        st.session_state.hasil_ai = response.text
    except:
        st.error("Gagal generate!")

if st.button("Generate Skrip"):
    if not produk:
        st.warning("⚠️ Nama Produk wajib diisi!")
    else:
        generate_content()

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

    st.markdown("<span class='label-box'>📸 visual konten</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='box-container'>{visual_text}</div>", unsafe_allow_html=True)

    st.markdown("<span class='label-box'>🎙️ teks voice over</span>", unsafe_allow_html=True)
    st.code(vo_text, language="text")

    col_re, col_done = st.columns(2)
    with col_re:
        if st.button("🔄 Coba Lagi", key="btn_lagi", use_container_width=True):
            generate_content()
            st.rerun()
    with col_done:
        if st.button("🗑️ Reset", key="btn_reset", use_container_width=True, on_click=reset_form):
            st.rerun()

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        <p>Built with ❤️ by <b>Cerita Ozi</b> | © 2026 Skripi Konten Team</p>
    </div>
    """, unsafe_allow_html=True)
