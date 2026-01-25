import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Affiliate Genie Pro", page_icon="🪄", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #FF4B4B;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        color: #333;
        white-space: pre-wrap;
    }
    .stTextArea textarea { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Affiliate Genie Pro")
st.write("Sekarang AI akan mengikuti kemauan dan situasi produkmu!")

# --- AREA INPUT ---
with st.container():
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
    
    produk = st.text_input("Nama Produk", placeholder="Contoh: Lap Microfiber Premium")
    
    # FITUR BARU: KONTEKS PRODUK
    konteks = st.text_area("Situasi / Kegunaan Spesifik (Opsional)", 
                           placeholder="Contoh: Fokus untuk bersihin dashboard mobil yang berdebu parah, atau untuk ngeringin piring di dapur tanpa ninggalin serat.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        # FITUR BARU: ANGLE KONTEN
        angle = st.selectbox("Angle Konten", ["Eksperimen/Tes", "Review Jujur", "Tips & Trik", "Storytelling", "Unboxing"])
    with col2:
        target_usia = st.selectbox("Target Usia", ["Gen Z", "Dewasa", "Orang Tua", "Umum"])
    with col3:
        durasi = st.selectbox("Durasi", ["20 detik", "30 detik", "45 detik", "60 detik"])

# --- LOGIKA GENERATE ---
if st.button("Generate Skrip Sesuai Keinginan ✨"):
    if not api_key or not produk:
        st.warning("Nama Produk dan API Key wajib diisi!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            prompt = f"""
            Tugas: Buat skrip affiliate video pendek (TikTok/Shopee).
            Produk: {produk}
            Konteks Spesifik: {konteks if konteks else 'Umum'}
            Angle Konten: {angle}
            Target Usia: {target_usia}
            Durasi Target: {durasi}

            Instruksi Khusus:
            1. Jika ada 'Konteks Spesifik', fokuslah pada situasi tersebut. Jangan bahas kegunaan lain yang tidak relevan.
            2. Sesuaikan pembukaan video dengan 'Angle Konten' {angle}.
            3. Struktur: HOOK (detik 1-3), MASALAH yang sesuai konteks, SOLUSI (keunggulan produk), dan CTA wajib "Klik keranjang di pojok kiri bawah sekarang!".
            4. Gunakan bahasa yang relate dengan {target_usia}.
            """
            
            with st.spinner('Menyesuaikan skrip dengan pikiranmu...'):
                response = model.generate_content(prompt)
                st.markdown(f"### 🎬 Skrip {angle} ({durasi})")
                st.markdown(f"""<div class="result-card">{response.text}</div>""", unsafe_allow_html=True)
                st.balloons()
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Gunakan kolom 'Situasi' untuk membedakan skrip satu produk yang punya banyak fungsi.")
