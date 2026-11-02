import streamlit as st
import json
import os
from datetime import date, time

st.set_page_config(
    page_title="MEDIBOX Dental",
    page_icon="🦷",
    layout="wide"
)

# PENYIMPANAN DATA
def baca_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []

def simpan_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

FILE_JADWAL = "jadwal_kontrol.json"
FILE_CATATAN = "catatan_perawatan.json"
FILE_OBAT = "pengingat_obat.json"

# DESAIN
st.markdown("""
<style>
.stApp {
    background-color: #F5F9FD;
}
section[data-testid="stSidebar"] {
    background-color: #E8F2FC;
}
h1, h2, h3 {
    color: #174A78;
}
.stButton > button {
    background-color: #2878B8;
    color: white;
    border-radius: 10px;
    border: none;
}
div[data-testid="stForm"] {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #DCE8F3;
}
</style>
""", unsafe_allow_html=True)

# MENU
st.sidebar.markdown("# 🦷 MEDIBOX")
st.sidebar.caption("Dental Care Assistant")
st.sidebar.divider()

menu = st.sidebar.radio(
    "MENU UTAMA",
    [
        "Beranda",
        "Jadwal Kontrol",
        "Cari Dokter",
        "Catatan Perawatan",
        "Pengingat Obat",
        "Pusat Edukasi",
        "Asisten Gigi"
    ]
)

st.sidebar.divider()
st.sidebar.caption("MEDIBOX Dental © 2026")

# BERANDA
if menu == "Beranda":

    st.title("Selamat Datang di MEDIBOX 🦷")
    st.write("Teman digital untuk membantu menjaga kesehatan gigi.")

    jadwal = baca_data(FILE_JADWAL)
    catatan = baca_data(FILE_CATATAN)
    obat = baca_data(FILE_OBAT)

    a, b, c = st.columns(3)
    a.metric("Total Jadwal", len(jadwal))
    b.metric("Catatan Perawatan", len(catatan))
    c.metric("Pengingat Obat", len(obat))

    st.divider()
    st.subheader("Layanan MEDIBOX")

    kolom = st.columns(3)
    layanan = [
        ("📅 Jadwal Kontrol", "Buat jadwal pemeriksaan gigi."),
        ("👨‍⚕️ Cari Dokter", "Lihat informasi dokter gigi."),
        ("📝 Catatan Perawatan", "Simpan riwayat perawatan."),
        ("💊 Pengingat Obat", "Catat jadwal penggunaan obat."),
        ("📚 Pusat Edukasi", "Pelajari kesehatan gigi."),
        ("💬 Asisten Gigi", "Dapatkan informasi kesehatan gigi.")
    ]

    for i, (judul, deskripsi) in enumerate(layanan):
        with kolom[i % 3]:
            st.markdown(f"### {judul}")
            st.write(deskripsi)

    st.info("Rawat kesehatan gigi dimulai dari kebiasaan baik.")

# JADWAL KONTROL
elif menu == "Jadwal Kontrol":

    st.title("📅 Jadwal Kontrol")
    st.write("Buat jadwal pemeriksaan gigi.")

    with st.form("form_jadwal"):
        nama = st.text_input("Nama Pasien")
        pemeriksa = st.text_input("Nama Dokter atau Pemeriksa")
        tanggal = st.date_input(
            "Tanggal Kontrol",
            min_value=date.today()
        )
        jam = st.time_input("Jam Kontrol", value=time(9, 0))
        keluhan = st.text_area("Keluhan atau Catatan")

        tombol = st.form_submit_button("Simpan Jadwal")

    if tombol:
        if nama.strip():
            data = baca_data(FILE_JADWAL)
            data.append({
                "nama": nama.strip(),
                "pemeriksa": pemeriksa,
                "tanggal": str(tanggal),
                "jam": str(jam),
                "keluhan": keluhan
            })
            simpan_data(FILE_JADWAL, data)
            st.success("Jadwal kontrol berhasil disimpan!")
        else:
            st.warning("Nama pasien harus diisi.")

    st.divider()
    st.subheader("Daftar Jadwal Kontrol")

    data = baca_data(FILE_JADWAL)

    if data:
        for i, item in enumerate(data):
            with st.expander(f"{item['nama']} - {item['tanggal']}"):
                st.write("Nama Pasien:", item["nama"])
                st.write("Pemeriksa:", item["pemeriksa"])
                st.write("Tanggal:", item["tanggal"])
                st.write("Jam:", item["jam"])
                st.write("Catatan:", item["keluhan"])

                if st.button("Hapus Jadwal", key=f"hapus_jadwal_{i}"):
                    data.pop(i)
                    simpan_data(FILE_JADWAL, data)
                    st.rerun()
    else:
        st.info("Belum ada jadwal kontrol.")

# CARI DOKTER
elif menu == "Cari Dokter":

    st.title("👨‍⚕️ Cari Dokter")
    st.write("Informasi dokter dan layanan pemeriksaan gigi.")

    st.info(
        "Fitur ini merupakan halaman informasi. "
        "Daftar dokter belum terhubung dengan data klinik."
    )

    st.subheader("Jenis Layanan")
    st.write("- Pemeriksaan gigi umum")
    st.write("- Konsultasi kesehatan gigi")
    st.write("- Pemeriksaan gusi")
    st.write("- Konsultasi perawatan gigi")

# CATATAN PERAWATAN
elif menu == "Catatan Perawatan":

    st.title("📝 Catatan Perawatan")
    st.write("Simpan catatan pemeriksaan dan perawatan gigi.")

    with st.form("form_catatan"):
        nama = st.text_input("Nama Pasien")
        tanggal = st.date_input("Tanggal Pemeriksaan")
        perawatan = st.text_input("Jenis Perawatan")
        keterangan = st.text_area("Keterangan")

        tombol = st.form_submit_button("Simpan Catatan")

    if tombol:
        if nama.strip() and perawatan.strip():
            data = baca_data(FILE_CATATAN)
            data.append({
                "nama": nama,
                "tanggal": str(tanggal),
                "perawatan": perawatan,
                "keterangan": keterangan
            })
            simpan_data(FILE_CATATAN, data)
            st.success("Catatan berhasil disimpan!")
        else:
            st.warning("Nama dan jenis perawatan harus diisi.")

    st.divider()
    st.subheader("Riwayat Perawatan")

    data = baca_data(FILE_CATATAN)

    if data:
        for i, item in enumerate(data):
            with st.expander(item["nama"] + " - " + item["tanggal"]):
                st.write("Perawatan:", item["perawatan"])
                st.write("Keterangan:", item["keterangan"])
                if st.button("Hapus Catatan", key=f"hapus_catatan_{i}"):
                    data.pop(i)
                    simpan_data(FILE_CATATAN, data)
                    st.rerun()
    else:
        st.info("Belum ada catatan perawatan.")

# PENGINGAT OBAT
elif menu == "Pengingat Obat":

    st.title("💊 Pengingat Obat")
    st.write("Catat informasi penggunaan obat.")

    with st.form("form_obat"):
        nama = st.text_input("Nama Pasien")
        obat = st.text_input("Nama Obat")
        jadwal = st.text_input("Jadwal Penggunaan")
        catatan = st.text_area("Catatan")

        tombol = st.form_submit_button("Simpan Pengingat")

    if tombol:
        if nama.strip() and obat.strip():
            data = baca_data(FILE_OBAT)
            data.append({
                "nama": nama,
                "obat": obat,
                "jadwal": jadwal,
                "catatan": catatan
            })
            simpan_data(FILE_OBAT, data)
            st.success("Pengingat berhasil disimpan!")
        else:
            st.warning("Nama pasien dan obat harus diisi.")

    st.divider()
    st.subheader("Daftar Pengingat")

    data = baca_data(FILE_OBAT)

    if data:
        for i, item in enumerate(data):
            with st.expander(item["nama"] + " - " + item["obat"]):
                st.write("Jadwal:", item["jadwal"])
                st.write("Catatan:", item["catatan"])
                if st.button("Hapus Pengingat", key=f"hapus_obat_{i}"):
                    data.pop(i)
                    simpan_data(FILE_OBAT, data)
                    st.rerun()
    else:
        st.info("Belum ada pengingat obat.")

# PUSAT EDUKASI
elif menu == "Pusat Edukasi":

    st.title("📚 Pusat Edukasi")
    st.write("Informasi sederhana untuk menjaga kesehatan gigi.")

    with st.expander("Cara menyikat gigi"):
        st.write(
            "Sikat gigi dua kali sehari menggunakan sikat berbulu "
            "lembut dan pasta gigi berfluorida."
        )

    with st.expander("Penyebab gigi berlubang"):
        st.write(
            "Gigi berlubang dapat disebabkan oleh plak dan bakteri "
            "yang mengolah gula menjadi asam."
        )

    with st.expander("Menjaga kesehatan gusi"):
        st.write(
            "Bersihkan sela gigi, sikat gigi dengan lembut, "
            "dan lakukan pemeriksaan rutin."
        )

    with st.expander("Kapan harus ke dokter gigi?"):
        st.write(
            "Lakukan pemeriksaan rutin dan konsultasikan jika "
            "mengalami nyeri, bengkak, atau keluhan pada gigi."
        )

# ASISTEN GIGI
elif menu == "Asisten Gigi":

    st.title("💬 Asisten Gigi")
    st.write("Pilih pertanyaan untuk mendapatkan informasi.")

    pertanyaan = st.selectbox(
        "Apa yang ingin kamu ketahui?",
        [
            "Berapa kali menyikat gigi dalam sehari?",
            "Bagaimana cara menjaga kesehatan gigi?",
            "Apa penyebab gigi berlubang?",
            "Bagaimana menjaga kesehatan gusi?",
            "Kapan harus memeriksakan gigi?"
        ]
    )

    jawaban = {
        "Berapa kali menyikat gigi dalam sehari?":
            "Sikat gigi dua kali sehari, pagi setelah sarapan "
            "dan malam sebelum tidur.",

        "Bagaimana cara menjaga kesehatan gigi?":
            "Sikat gigi secara rutin, bersihkan sela gigi, "
            "dan lakukan pemeriksaan berkala.",

        "Apa penyebab gigi berlubang?":
            "Gigi berlubang berkaitan dengan plak, bakteri, "
            "dan paparan gula.",

        "Bagaimana menjaga kesehatan gusi?":
            "Sikat gigi dengan lembut dan bersihkan sela gigi.",

        "Kapan harus memeriksakan gigi?":
            "Periksa secara rutin dan segera konsultasikan "
            "jika muncul keluhan."
    }

    st.info(jawaban[pertanyaan])
    st.caption(
        "Informasi ini bersifat edukasi dan bukan pengganti "
        "pemeriksaan dokter gigi."
    )