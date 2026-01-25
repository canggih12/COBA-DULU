import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Affiliate Genie AI", page_icon="🪄")

# --- SIDEBAR: Setting API Key ---
with st.sidebar:
    st.title("Pengaturan")
    api_key = "AIzaSyCaSLrhJgnx6Ok5RKItn1pCf4zyPcA45Ds"
    st.info("Dapatkan API Key di Google AI Studio")

# --- MAIN UI ---
st.title("🪄 Affiliate Content Genie")
st.write("Masukkan nama produk, dan biarkan AI meracik skrip konten yang menjual untukmu.")

produk = st.text_input("Nama Produk", placeholder="Contoh: Powerbank 20.000mAh Mini")
gaya_bahasa = st.selectbox("Gaya Bahasa", ["Santai/Gokil", "Edukasi/Serius", "Review Jujur", "Hard Sell"])

if st.button("Generate Ide Konten ✨"):
    if not api_key:
        st.error("Silakan masukkan API Key di sidebar kiri dulu ya!")
    elif not produk:
        st.warning("Nama produknya diisi dulu boss!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Kamu adalah ahli copywriting affiliate TikTok dan Instagram. 
            Buatkan skrip konten untuk produk: {produk}.
            Gunakan gaya bahasa: {gaya_bahasa}.
            Format harus terdiri dari:
            1. **HOOK**: Kalimat pembuka yang bikin orang berhenti scrolling.
            2. **MASALAH**: Singgung keresahan yang dialami calon pembeli.
            3. **SOLUSI/VALUE**: Kenapa produk {produk} ini wajib dibeli.
            4. **CTA**: Ajakan beli di keranjang kuning atau klik link di bio.
            """
            
            with st.spinner('Genie sedang meracik kata-kata...'):
                response = model.generate_content(prompt)
                st.subheader("Hasil Racikan AI:")
                st.markdown(response.text)
                st.balloons()
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
