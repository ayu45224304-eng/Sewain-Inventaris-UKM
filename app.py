"""Sewain: sistem penyewaan inventaris UKM."""
import streamlit as st

st.set_page_config(
    page_title="Sewain",
    page_icon=":material/inventory_2:",
    layout="wide",
    initial_sidebar_state="expanded",
)

from core import db, styles
from core.utils import HALAMAN
from views import dashboard, data_penyewa, inventaris, laporan, login, penyewaan_baru, pengembalian, riwayat, tentang

styles.inject()
db.init_db()
if not st.session_state.get("pengguna"):
    login.render()
    st.stop()
st.markdown(
    """
    <style>
    [data-testid="stDataObjectViz"] th,
    div[data-testid="stTable"] th,
    [data-testid="stDataFrame"] [role="columnheader"],
    [data-testid="stDataFrame"] [role="columnheader"] *,
    [data-testid="stDataEditor"] [role="columnheader"],
    [data-testid="stDataEditor"] [role="columnheader"] * {
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

RUTE = {
    HALAMAN[0]: dashboard.render,
    HALAMAN[1]: penyewaan_baru.render,
    HALAMAN[2]: pengembalian.render,
    HALAMAN[3]: riwayat.render,
    HALAMAN[4]: laporan.render,
    HALAMAN[5]: inventaris.render,
    HALAMAN[6]: data_penyewa.render,
    HALAMAN[7]: tentang.render,
}


def _navigasi(halaman):
    if st.session_state.get("nav") != halaman:
        st.session_state.pop("last_return_code", None)
    st.session_state["nav"] = halaman


def _logout():
    st.session_state.pop("pengguna", None)
    st.session_state.pop("login_failures", None)
    st.session_state.pop("login_locked_until", None)


@st.dialog("Ubah Password")
def _ubah_password():
    st.caption("Password baru minimal 8 karakter.")
    with st.form("form_ubah_password"):
        password_lama = st.text_input(
            "Password lama",
            type="password",
            autocomplete="current-password",
        )
        password_baru = st.text_input(
            "Password baru",
            type="password",
            autocomplete="new-password",
        )
        konfirmasi_password = st.text_input(
            "Konfirmasi password baru",
            type="password",
            autocomplete="new-password",
        )
        submitted = st.form_submit_button("Simpan Password", type="primary")

    if submitted:
        try:
            db.change_password(
                st.session_state["pengguna"]["id"],
                password_lama,
                password_baru,
                konfirmasi_password,
            )
        except ValueError as error:
            st.error(str(error))
        else:
            st.success("Password berhasil diperbarui.")


st.session_state.setdefault("nav", HALAMAN[0])
if st.session_state["nav"] not in RUTE:
    st.session_state["nav"] = HALAMAN[0]
with st.sidebar:
    st.markdown("""
        <div class="brand">
            <div class="brand-logo"><span class="material-symbols-rounded">inventory_2</span></div>
            <div><div class="brand-name">Sewain</div><div class="brand-sub">INVENTARIS • UKM</div></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("### Menu Utama")
    ikon_navigasi = [
        ":material/dashboard:",
        ":material/post_add:",
        ":material/assignment_return:",
        ":material/history:",
        ":material/analytics:",
        ":material/inventory_2:",
        ":material/groups:",
        ":material/info:",
    ]
    for halaman, ikon in zip(HALAMAN, ikon_navigasi):
        st.button(
            halaman,
            key=f"nav_{halaman}",
            icon=ikon,
            type="primary" if st.session_state["nav"] == halaman else "secondary",
            width="stretch",
            on_click=_navigasi,
            args=(halaman,),
        )
    st.divider()
    st.markdown('<div class="sidebar-info"><span class="online-dot"></span> <b>Sistem Penyewaan UKM</b></div>', unsafe_allow_html=True)
    pengguna = st.session_state["pengguna"]
    st.markdown('<div class="sidebar-account"><b>Akun aktif</b></div>', unsafe_allow_html=True)
    st.write(f"**{pengguna['nama_lengkap']}**")
    st.caption(f"@{pengguna['username']}")
    if st.button("Ubah Password", icon=":material/key:", width="stretch"):
        _ubah_password()
    if st.button("Logout", icon=":material/logout:", width="stretch"):
        _logout()
        st.rerun()

RUTE[st.session_state["nav"]]()
