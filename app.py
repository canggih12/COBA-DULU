import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="IDE KONTEN AFFILIATE", page_icon="🪄", layout="centered")

# Custom CSS untuk UI yang lebih clean
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
    }
    </style>
    """, unsafe_allow_html=True)

st.title("GENERATOR IDE KONTEN")
st.write("Racik skrip konten viral yang pas dengan durasi dan target audiensmu.")

# --- AREA INPUT ---
with st.container():
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
    st.sidebar.info("Gunakan Gemini 3 Flash Preview untuk hasil terbaik.")
    
    produk = st.text_input("Nama Produk", placeholder="Contoh: Blender Portable Mini")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        target_usia = st.selectbox(
            "Target Usia", 
            ["Gen Z (15-24)", "Dewasa (25-35)", "Orang Tua (35+)", "Umum"]
        )
    with col2:
        durasi = st.selectbox("Durasi Video", ["20 detik", "30 detik", "45 detik", "60 detik"])
    with col3:
        gaya_bahasa = st.selectbox("Tone", ["Santai", "Informatif", "Hard Sell"])

# --- LOGIKA GENERATE ---
if st.button("Generate Skrip Viral ✨"):
    if not api_key or not produk:
        st.warning("Pastikan Nama Produk dan API Key sudah terisi!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            # Prompt yang disesuaikan dengan Durasi
            prompt = f"""
            Tugas: Buat skrip konten video pendek (TikTok/Shopee).
            Produk: {produk}
            Target Usia: {target_usia}
            Durasi Target: {durasi}
            Gaya Bahasa: {gaya_bahasa}

            Instruksi Khusus:
            1. Sesuaikan panjang kalimat agar pas dibacakan dalam waktu {durasi}.
            2. Kosa kata harus relevan dengan {target_usia}.
            3. Struktur wajib:
               - HOOK: Instan memicu penasaran.
               - MASALAH: Singkat & relate.
               - SOLUSI: Mengapa {produk} adalah jawabannya.
               - CTA: Wajib sebut "Klik keranjang di pojok kiri bawah sekarang juga!".
            4. Berikan estimasi pembagian waktu di setiap bagian (misal: [00:00-00:05] Hook).
            """
            
            with st.spinner(f'Menyusun skrip {durasi}...'):
                response = model.generate_content(prompt)
                
                st.markdown(f"### 🎬 Skrip Konten ({durasi})")
                st.markdown(f"""<div class="result-card">{response.text}</div>""", unsafe_allow_html=True)
                st.balloons()
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Tips: Untuk durasi 20 detik, fokuslah pada Hook dan CTA yang kuat.")
