import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fungsi utilitas untuk menghitung rata-rata dari input teks
def hitung_rerata_kebisingan(teks_input):
    try:
        nilai_list = [float(i.strip()) for i in teks_input.split(",") if i.strip() != ""]
        if nilai_list:
            rata2 = sum(nilai_list) / len(nilai_list)
            return rata2, nilai_list
        else:
            return None, []
    except ValueError:
        return None, []

# Fungsi untuk menampilkan cara pencegahan
def tampilkan_cara_pencegahan(jenis_lingkungan):
    if jenis_lingkungan == "lingkungan kerja":
        st.markdown("""
        ### 🛡️ Cara Pencegahan:
        - Gunakan **alat pelindung telinga** (earplug/earmuff) di area kerja bising.
        - **Kurangi waktu paparan** pekerja di lingkungan dengan kebisingan tinggi.
        - Gunakan **peredam suara** pada mesin dan ruangan kerja.
        - Lakukan **pengaturan rotasi kerja** agar paparan tidak terus-menerus.
        - Terapkan **pengawasan rutin** tingkat kebisingan oleh petugas K3.
        """)

    elif jenis_lingkungan == "kawasan khusus":
        st.markdown("""
        ### 🛡️ Cara Pencegahan:
        - **Atur ulang tata letak** agar aktivitas bising terpisah dari publik.
        - Gunakan **material peredam suara** pada bangunan dan kendaraan.
        - Terapkan **jam operasional yang terjadwal** untuk aktivitas bising.
        - Lakukan **pengawasan terhadap sumber kebisingan** seperti speaker, kendaraan, atau mesin.
        """)

    elif jenis_lingkungan == "lingkungan kegiatan":
        st.markdown("""
        ### 🛡️ Cara Pencegahan:
        - **Gunakan jendela dan pintu kedap suara** untuk mengurangi kebisingan luar.
        - **Pindahkan sumber suara** seperti TV/speaker dari dinding yang berdekatan dengan ruang istirahat.
        - Tanam **vegetasi atau pagar hijau** sebagai penghalang suara dari jalan atau lingkungan ramai.
        - Terapkan **jam tenang** khususnya di area sekolah, rumah sakit, dan tempat ibadah.
        """)

# Judul aplikasi
st.markdown("""
    <h1 style='text-align: center; color: #5EFF33; animation: fadeIn 2s ease-in;'>🔊 Kalkulator Kebisingan</h1>
    <style>
        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
        h1 {
            animation: fadeIn 2s ease-in;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar menu
menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Beranda",
        "Kalkulator Lingkungan Kerja",
        "Kalkulator Kawasan Khusus",
        "Kalkulator Lingkungan Kegiatan",
        "Tentang",
    ],
)

if menu == "Beranda":
    st.subheader("Selamat Datang di Kalkulator Kebisingan")
    st.write("""
        Aplikasi ini digunakan untuk mengevaluasi apakah tingkat kebisingan memenuhi standar SNI di berbagai lingkungan:
        - **Umum / Lingkungan Kerja**: Maks. 85 dB
        - **Kawasan Khusus**: Maks. 70 dB
        - **Lingkungan Kegiatan**: Maks. 55 dB
    """)
    st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTdndHhjOGo3eHpjbGxxMGp1cm0wamU2MG4xbXV6bjdha3JtMXplZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5mYcsVrgxtxt7QUc55/giphy.gif", use_container_width=True)

elif menu == "Kalkulator Lingkungan Kerja":
    st.subheader("Kalkulator Kebisingan untuk Lingkungan Kerja")
    SNI_LIMIT = 85.0

    st.write("Masukkan satu atau beberapa nilai kebisingan (`dB`), pisahkan dengan koma (`,`) jika lebih dari satu data:")
    input_data = st.text_area("Contoh: 80, 82.5, 79", "")

    if input_data:
        rata2, semua_nilai = hitung_rerata_kebisingan(input_data)
        if rata2 is not None:
            st.write(f"📊 Data kebisingan yang dimasukkan: {semua_nilai}")
            st.write(f"📉 Rata-rata kebisingan: **{rata2:.2f} dB**")

            # Plot grafik
            fig, ax = plt.subplots()
            index = np.arange(len(semua_nilai))
            ax.bar(index, semua_nilai, color='skyblue')
            ax.axhline(SNI_LIMIT, color='red', linestyle='--', label=f'Batas SNI ({SNI_LIMIT} dB)')
            ax.set_xlabel('Data ke-')
            ax.set_ylabel('Tingkat Kebisingan (dB)')
            ax.set_title('Visualisasi Data Kebisingan')
            ax.set_xticks(index)
            ax.set_xticklabels([str(i+1) for i in index])
            ax.legend()
            st.pyplot(fig)
            import io
            from matplotlib.backends.backend_pdf import PdfPages

            # Buat DataFrame untuk ekspor
            df = pd.DataFrame({
                "Data ke-": [f"{i+1}" for i in range(len(semua_nilai))],
                "Nilai Kebisingan (dB)": semua_nilai
            })

            # Tombol download CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Unduh Data sebagai CSV",
                data=csv_buffer.getvalue(),
                file_name="data_kebisingan_lingkungan_kerja.csv",
                mime="text/csv"
            )

            # Tombol download PDF (dengan grafik)
            pdf_buffer = io.BytesIO()
            with PdfPages(pdf_buffer) as pdf:
                fig_pdf, ax_pdf = plt.subplots()
                ax_pdf.bar(range(len(semua_nilai)), semua_nilai, color='skyblue')
                ax_pdf.axhline(SNI_LIMIT, color='red', linestyle='--', label=f'Batas SNI ({SNI_LIMIT} dB)')
                ax_pdf.set_title('Grafik Kebisingan - Lingkungan Kerja')
                ax_pdf.set_xlabel('Data ke-')
                ax_pdf.set_ylabel('dB')
                ax_pdf.set_xticks(range(len(semua_nilai)))
                ax_pdf.set_xticklabels([str(i+1) for i in range(len(semua_nilai))])
                ax_pdf.legend()
                pdf.savefig(fig_pdf)
                plt.close(fig_pdf)

             # Tambahkan halaman dengan ringkasan teks
            from matplotlib.figure import Figure
            fig_text = Figure(figsize=(8.27, 11.69))  # A4 size
            ax_text = fig_text.subplots()
            ax_text.axis('off')
            summary = (
                f"📄 Ringkasan Analisis Kebisingan Lingkungan Kerja\n\n"
                f"Jumlah Data: {len(semua_nilai)}\n"
                f"Rata-rata: {rata2:.2f} dB\n"
                f"Standar Batas SNI: {SNI_LIMIT} dB\n"
                f"Status: {'MEMENUHI' if rata2 <= SNI_LIMIT else 'TIDAK MEMENUHI'}\n\n"
                f"Data:\n"
                + "\n".join([f"{i+1}. {val} dB" for i, val in enumerate(semua_nilai)])
            )
            ax_text.text(0, 1, summary, va='top', fontsize=10)
            pdf.savefig(fig_text)

            st.download_button(
                label="📄 Unduh Laporan PDF",
                data=pdf_buffer.getvalue(),
                file_name="laporan_kebisingan_lingkungan_kerja.pdf",
                mime="application/pdf"
            )


            if rata2 <= SNI_LIMIT:
                st.success(f"{rata2:.2f} dB ✅ MEMENUHI standar SNI lingkungan kerja (≤ {SNI_LIMIT} dB).")
                st.info("**Keterangan:** Tingkat kebisingan dalam batas aman. Risiko terhadap gangguan pendengaran rendah.")
            else:
                st.error(f"{rata2:.2f} dB ❌ TIDAK MEMENUHI standar SNI lingkungan kerja (> {SNI_LIMIT} dB).")
                st.warning("**Dampak Potensial:** Dapat menyebabkan gangguan pendengaran, stres, kelelahan, dan menurunkan produktivitas kerja bila terpapar dalam waktu lama.")
                tampilkan_cara_pencegahan("lingkungan kerja")

        else:
            st.error("Format input tidak valid. Pastikan hanya memasukkan angka dan koma.")
    else:
        st.info("Silakan masukkan nilai tingkat kebisingan terlebih dahulu.")

elif menu == "Kalkulator Kawasan Khusus":
    st.subheader("Kalkulator Kebisingan untuk kawasan perdagangan, tempat rekreasi, bandara, stasiun, terminal, pelabuhan dan sejenisnya")
    SNI_LIMIT = 70.0

    st.write("Masukkan satu atau beberapa nilai kebisingan (`dB`), pisahkan dengan koma (`,`) jika lebih dari satu data:")
    input_data = st.text_area("Contoh: 42, 43.5, 46", "")

    if input_data:
        rata2, semua_nilai = hitung_rerata_kebisingan(input_data)
        if rata2 is not None:
            st.write(f"📊 Data kebisingan yang dimasukkan: {semua_nilai}")
            st.write(f"📉 Rata-rata kebisingan: **{rata2:.2f} dB**")
            import io
            from matplotlib.backends.backend_pdf import PdfPages

            # Buat DataFrame untuk ekspor
            df = pd.DataFrame({
                "Data ke-": [f"{i+1}" for i in range(len(semua_nilai))],
                "Nilai Kebisingan (dB)": semua_nilai
            })

            # Tombol download CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Unduh Data sebagai CSV",
                data=csv_buffer.getvalue(),
                file_name="data_kebisingan_kawasan_khusus.csv",
                mime="text/csv"
            )

            # Tombol download PDF (dengan grafik)
            pdf_buffer = io.BytesIO()
            with PdfPages(pdf_buffer) as pdf:
                fig_pdf, ax_pdf = plt.subplots()
                ax_pdf.bar(range(len(semua_nilai)), semua_nilai, color='lightgreen')
                ax_pdf.axhline(SNI_LIMIT, color='red', linestyle='--', label=f'Batas SNI ({SNI_LIMIT} dB)')
                ax_pdf.set_title('Grafik Kebisingan - Kawasan Khusus')
                ax_pdf.set_xlabel('Data ke-')
                ax_pdf.set_ylabel('dB')
                ax_pdf.set_xticks(range(len(semua_nilai)))
                ax_pdf.set_xticklabels([str(i+1) for i in range(len(semua_nilai))])
                ax_pdf.legend()
                pdf.savefig(fig_pdf)
                plt.close(fig_pdf)

                # Ringkasan teks ke PDF
                from matplotlib.figure import Figure
                fig_text = Figure(figsize=(8.27, 11.69))  # A4
                ax_text = fig_text.subplots()
                ax_text.axis('off')
                summary = (
                    f"📄 Ringkasan Analisis Kebisingan Kawasan Khusus\n\n"
                    f"Jumlah Data: {len(semua_nilai)}\n"
                    f"Rata-rata: {rata2:.2f} dB\n"
                    f"Standar Batas SNI: {SNI_LIMIT} dB\n"
                    f"Status: {'MEMENUHI' if rata2 <= SNI_LIMIT else 'TIDAK MEMENUHI'}\n\n"
                    f"Data:\n"
                    + "\n".join([f"{i+1}. {val} dB" for i, val in enumerate(semua_nilai)])
                )
                ax_text.text(0, 1, summary, va='top', fontsize=10)
                pdf.savefig(fig_text)

            st.download_button(
                label="📄 Unduh Laporan PDF",
                data=pdf_buffer.getvalue(),
                file_name="laporan_kebisingan_kawasan_khusus.pdf",
                mime="application/pdf"
            )

            # Plot grafik
            fig, ax = plt.subplots()
            index = np.arange(len(semua_nilai))
            ax.bar(index, semua_nilai, color='lightgreen')
            ax.axhline(SNI_LIMIT, color='red', linestyle='--', label=f'Batas SNI ({SNI_LIMIT} dB)')
            ax.set_xlabel('Data ke-')
            ax.set_ylabel('Tingkat Kebisingan (dB)')
            ax.set_title('Visualisasi Data Kebisingan Kawasan Khusus')
            ax.set_xticks(index)
            ax.set_xticklabels([str(i+1) for i in index])
            ax.legend()
            st.pyplot(fig)

            if rata2 <= SNI_LIMIT:
                st.success(f"{rata2:.2f} dB ✅ MEMENUHI standar SNI Kawasan Khusus (≤ {SNI_LIMIT} dB).")
                st.info("**Keterangan:** Kebisingan dalam batas wajar pada kawasan yang ramai. Risiko terhadap kecelakaan rendah.")
            else:
                st.error(f"{rata2:.2f} dB ❌ TIDAK MEMENUHI standar SNI Kawasan Khusus (> {SNI_LIMIT} dB).")
                st.warning("**Dampak Potensial:** Dapat mengganggu konsentrasi, menambah risiko kecelakaan yang tidak terduga, dan menambah stres.")
                tampilkan_cara_pencegahan("kawasan khusus")
        else:
            st.error("Format input tidak valid. Pastikan hanya memasukkan angka dan koma.")
    else:
        st.info("Silakan masukkan nilai tingkat kebisingan terlebih dahulu.")

elif menu == "Kalkulator Lingkungan Kegiatan":
    st.subheader("Kalkulator Kebisingan untuk lingkungan rumah, sekolah, rumah sakit, tempat ibadah dan sejenisnya")
    SNI_LIMIT = 55.0

    st.write("Masukkan satu atau beberapa nilai kebisingan (`dB`), pisahkan dengan koma (`,`) jika lebih dari satu data:")
    input_data = st.text_area("Contoh: 50, 53, 57", "")

    if input_data:
        rata2, semua_nilai = hitung_rerata_kebisingan(input_data)
        if rata2 is not None:
            st.write(f"📊 Data kebisingan yang dimasukkan: {semua_nilai}")
            st.write(f"📉 Rata-rata kebisingan: **{rata2:.2f} dB**")
            import io
            from matplotlib.backends.backend_pdf import PdfPages

            # Buat DataFrame
            df = pd.DataFrame({
                "Data ke-": [f"{i+1}" for i in range(len(semua_nilai))],
                "Nilai Kebisingan (dB)": semua_nilai
            })

            # Tombol download CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Unduh Data sebagai CSV",
                data=csv_buffer.getvalue(),
                file_name="data_kebisingan_lingkungan_kegiatan.csv",
                mime="text/csv"
            )

            # Tombol download PDF (grafik + ringkasan)
            pdf_buffer = io.BytesIO()
            with PdfPages(pdf_buffer) as pdf:
                fig_pdf, ax_pdf = plt.subplots()
                ax_pdf.bar(range(len(semua_nilai)), semua_nilai, color='lightcoral')
                ax_pdf.axhline(SNI_LIMIT, color='red', linestyle='--', label=f'Batas SNI ({SNI_LIMIT} dB)')
                ax_pdf.set_title('Grafik Kebisingan - Lingkungan Kegiatan')
                ax_pdf.set_xlabel('Data ke-')
                ax_pdf.set_ylabel('dB')
                ax_pdf.set_xticks(range(len(semua_nilai)))
                ax_pdf.set_xticklabels([str(i+1) for i in range(len(semua_nilai))])
                ax_pdf.legend()
                pdf.savefig(fig_pdf)
                plt.close(fig_pdf)

                # Ringkasan teks PDF
                from matplotlib.figure import Figure
                fig_text = Figure(figsize=(8.27, 11.69))
                ax_text = fig_text.subplots()
                ax_text.axis('off')
                summary = (
                    f"📄 Ringkasan Analisis Kebisingan Lingkungan Kegiatan\n\n"
                    f"Jumlah Data: {len(semua_nilai)}\n"
                    f"Rata-rata: {rata2:.2f} dB\n"
                    f"Standar Batas SNI: {SNI_LIMIT} dB\n"
                    f"Status: {'MEMENUHI' if rata2 <= SNI_LIMIT else 'TIDAK MEMENUHI'}\n\n"
                    f"Data:\n"
                    + "\n".join([f"{i+1}. {val} dB" for i, val in enumerate(semua_nilai)])
                )
                ax_text.text(0, 1, summary, va='top', fontsize=10)
                pdf.savefig(fig_text)

            st.download_button(
                label="📄 Unduh Laporan PDF",
                data=pdf_buffer.getvalue(),
                file_name="laporan_kebisingan_lingkungan_kegiatan.pdf",
                mime="application/pdf"
            )

            # Plot grafik
            fig, ax = plt.subplots()
            index = np.arange(len(semua_nilai))
            ax.bar(index, semua_nilai, color='orange')
            ax.axhline(SNI_LIMIT, color='red', linestyle='--', label=f'Batas SNI ({SNI_LIMIT} dB)')
            ax.set_xlabel('Data ke-')
            ax.set_ylabel('Tingkat Kebisingan (dB)')
            ax.set_title('Visualisasi Data Kebisingan Rumah')
            ax.set_xticks(index)
            ax.set_xticklabels([str(i+1) for i in index])
            ax.legend()
            st.pyplot(fig)

            if rata2 <= SNI_LIMIT:
                st.success(f"{rata2:.2f} dB ✅ MEMENUHI standar SNI lingkungan kegiatan (≤ {SNI_LIMIT} dB).")
                st.info("**Keterangan:** Suasana dalam batas kebisingan yang nyaman dan aman untuk istirahat dan kegiatan lainnya.")
            else:
                st.error(f"{rata2:.2f} dB ❌ TIDAK MEMENUHI standar SNI lingkungan kegiatan (> {SNI_LIMIT} dB).")
                st.warning("**Dampak Potensial:** Dapat menyebabkan gangguan tidur dan kecemasan, tekanan darah meningkat, stres psikologis, dan penurunan kualitas hidup.")
                tampilkan_cara_pencegahan("lingkungan kegiatan")
        else:
            st.error("Format input tidak valid. Pastikan hanya memasukkan angka dan koma.")
    else:
        st.info("Silakan masukkan nilai tingkat kebisingan terlebih dahulu.")

elif menu == "Tentang":
    st.subheader("Tentang Aplikasi")
    st.write(
        """
        Aplikasi ini membantu mengevaluasi tingkat kebisingan di berbagai lingkungan berdasarkan Standar Nasional Indonesia (SNI).
        """
    )

    st.markdown("### 📚 Referensi Standar Resmi:")

    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown("**Lingkungan Kerja / Umum**  \nSNI 7231:2009 - Metoda Pengukuran Intensitas Kebisingan di Tempat Kerja")
    with col2:
        st.link_button("🌐 Lihat referensi", "https://jdih.kemnaker.go.id/asset/data_puu/Permen_5_2018.pdf")

    col3, col4 = st.columns([0.7, 0.3])
    with col3:
        st.markdown("**Kawasan Khusus dan Lingkungan Kegiatan**  \nSNI 03-6386-2000 - Spesifikasi Tingkat Bunyi dan Waktu Dengung dalam Bangunan Gedung dan Perumahan")
    with col4:
        st.link_button("🌐 Lihat referensi", "https://ppkl.menlhk.go.id/website/filebox/723/190930165749Kepmen%20LH%2048%20Tahun%201996.pdf")

    st.markdown("""
        <br><hr>
        🧑‍🎓 **Tugas Akhir Mata Kuliah Logika dan Pemrograman Komputer**  
        1F Pengolahan Limbah Industri - Politeknik AKA Bogor  
        _Dikembangkan dengan Python & Streamlit._
    """, unsafe_allow_html=True)
