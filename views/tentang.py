"""Halaman informasi aplikasi Sewain."""
import pandas as pd
import streamlit as st

from views.common import header


ANGGOTA_PENYUSUN = [
    {"NO": 1, "NAMA": "Alvina Anggi Fitria", "NIM": "4.52.24.3.01"},
    {"NO": 2, "NAMA": "Ayu Wulandari", "NIM": "4.52.24.3.04"},
    {"NO": 3, "NAMA": "Mei Saroh", "NIM": "4.52.24.3.16"},
    {"NO": 4, "NAMA": "Nailil Muna", "NIM": "4.52.24.3.20"},
]


def render():
    header(
        "TENTANG",
        "Tentang Sewain",
        "Sistem Administrasi Penyewaan Inventaris UKM.",
    )

    with st.container(border=True):
        st.subheader("Tentang aplikasi")
        st.write(
            "Sewain adalah sistem administrasi penyewaan inventaris UKM. "
            "Aplikasi ini membantu admin mencatat penyewaan dan pengembalian "
            "barang, memantau stok dan keterlambatan, mengelola data penyewa, "
            "serta mengunduh nota dan laporan dalam satu tempat."
        )

    with st.container(border=True):
        st.subheader("Tim penyusun")
        st.write("Kelompok 5")
        anggota = pd.DataFrame(ANGGOTA_PENYUSUN, columns=["NO", "NAMA", "NIM"])
        st.dataframe(
            anggota,
            column_config={
                "NO": st.column_config.NumberColumn("NO", format="%d", alignment="center"),
                "NAMA": st.column_config.TextColumn("NAMA", alignment="left"),
                "NIM": st.column_config.TextColumn("NIM", alignment="center"),
            },
            hide_index=True,
            height="auto",
        )

    with st.container(border=True):
        st.subheader("Kontak")
        st.markdown("**Email**")
        st.markdown(
            "[sewain.inventaris.ukm@gmail.com](mailto:sewain.inventaris.ukm@gmail.com)"
        )
