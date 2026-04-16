import streamlit as st
from openai import OpenAI

# 1. Konfigurasi OpenRouter
# Ganti dengan API Key OpenRouter Anda
OPENROUTER_API_KEY = "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"  # Contoh API Key, pastikan untuk menyimpan dengan aman dan tidak membagikannya secara publik

# Inisialisasi klien OpenAI yang diarahkan ke server OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# 2. Antarmuka Web Streamlit
st.set_page_config(page_title="AI Evaluator", page_icon="🎓")
st.title("🎓 Reviewer Judul Skripsi Prodi Sistem Informasi Unpam")
#st.write("Menggunakan model Llama-3")

# Form Input
judul_mahasiswa = st.text_input("Judul Tugas Akhir:", placeholder="Input Tema/Judul Tugas Akhir")
deskripsi_singkat = st.text_area("Deskripsi Singkat:", placeholder="Input latar belakang")

# 3. Logika Pemrosesan AI
if st.button("Analisis Judul", type="primary"):
    if judul_mahasiswa:
        with st.spinner("Kami sedang mengevaluasi judul Anda..."):
            
            # System Prompt (Aturan/Otak Kampus Anda)
            system_prompt = """
            Kamu adalah Mesin Evaluator Judul Skripsi di Prodi Sistem Informasi.
            Gunakan ATURAN KAMPUS berikut:
            1. Judul berupa aplikasi CRUD (Sistem Informasi Penjualan/Perpustakaan/Absensi) tanpa analitik atau metode spesifik -> KEPUTUSAN: TOLAK.
            2. Judul menggunakan algoritma/SPK tapi metode tidak disebutkan -> KEPUTUSAN: REVISI.
            3. Judul mencakup Audit IT, Enterprise Architecture, Machine Learning, atau Tata Kelola IT -> KEPUTUSAN: TERIMA.
            
            Berikan output terstruktur:
            - KEPUTUSAN: [Terima / Tolak / Revisi]
            - KOREKSI: [Kritik akademis secara tajam namun membangun]
            - SARAN: [Rekomendasi spesifik untuk menaikkan level judul]
            """
            
            user_prompt = f"Judul: {judul_mahasiswa}\nDeskripsi: {deskripsi_singkat}"
            
            try:
                # Memanggil API OpenRouter (menggunakan model Llama-3 versi gratis)
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b:free",  # Pastikan model ini masih aktif dan gratis di OpenRouter
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    # Temperatur rendah agar jawaban tidak terlalu melenceng/kreatif (konsisten)
                    temperature=0.3 
                )
                
                # Menampilkan Hasil
                st.subheader("📊 Hasil Evaluasi")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Mohon masukkan judul tugas akhir terlebih dahulu!")
