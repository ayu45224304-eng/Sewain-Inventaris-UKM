import time

import streamlit as st

from core import db

MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCK_SECONDS = 60


def _simpan_sesi(pengguna):
    st.session_state["pengguna"] = pengguna
    st.session_state.pop("login_failures", None)
    st.session_state.pop("login_locked_until", None)
    st.rerun()


def render():
    _, form_column, _ = st.columns([1, 1.6, 1], gap="large")
    with form_column:
        _, logo_column, _ = st.columns([1, 2, 1])
        with logo_column:
            st.image("assets/sewain_logo_transparent.png", width=180)
        st.markdown(
            '<div class="login-heading">Selamat Datang di Sewain</div>'
            '<div class="login-subtitle">Sistem Penyewaan Inventaris UKM</div>',
            unsafe_allow_html=True,
        )

        tab_masuk, tab_daftar = st.tabs(["Masuk", "Daftar"])

        with tab_masuk:
            with st.container(border=True):
                remaining_lock = max(
                    0,
                    int(st.session_state.get("login_locked_until", 0) - time.time()),
                )
                locked = remaining_lock > 0
                if locked:
                    st.warning(
                        f"Terlalu banyak percobaan gagal. Silakan coba lagi dalam "
                        f"{remaining_lock} detik."
                    )

                with st.form("login_form"):
                    username = st.text_input(
                        "Username",
                        key="login_username",
                        autocomplete="username",
                    )
                    password = st.text_input(
                        "Password",
                        key="login_password",
                        type="password",
                        autocomplete="current-password",
                    )
                    submitted = st.form_submit_button(
                        "Masuk",
                        type="primary",
                        width="stretch",
                        disabled=locked,
                    )

                if submitted:
                    pengguna = db.authenticate(username, password)
                    if pengguna is None:
                        failures = st.session_state.get("login_failures", 0) + 1
                        st.session_state["login_failures"] = failures
                        if failures >= MAX_LOGIN_ATTEMPTS:
                            st.session_state["login_locked_until"] = (
                                time.time() + LOGIN_LOCK_SECONDS
                            )
                            st.session_state["login_failures"] = 0
                            st.error(
                                "Username atau password salah. Akses login dikunci "
                                f"selama {LOGIN_LOCK_SECONDS} detik."
                            )
                        else:
                            st.error("Username atau password salah.")
                    else:
                        _simpan_sesi(pengguna)

        with tab_daftar:
            with st.container(border=True):
                st.caption("Buat akun baru untuk mengakses Sewain.")
                with st.form("register_form"):
                    nama_lengkap = st.text_input(
                        "Nama lengkap",
                        key="register_nama_lengkap",
                        autocomplete="name",
                    )
                    username_baru = st.text_input(
                        "Username",
                        key="register_username",
                        autocomplete="username",
                    )
                    password_baru = st.text_input(
                        "Password",
                        key="register_password",
                        type="password",
                        autocomplete="new-password",
                    )
                    konfirmasi_password = st.text_input(
                        "Konfirmasi password",
                        key="register_password_confirmation",
                        type="password",
                        autocomplete="new-password",
                    )
                    submitted_daftar = st.form_submit_button(
                        "Daftar",
                        type="primary",
                        width="stretch",
                    )

                if submitted_daftar:
                    try:
                        pengguna = db.register_user(
                            username_baru,
                            password_baru,
                            konfirmasi_password,
                            nama_lengkap,
                        )
                    except ValueError as error:
                        st.error(str(error))
                    else:
                        st.success("Akun berhasil dibuat. Mengalihkan ke aplikasi.")
                        _simpan_sesi(pengguna)

        st.markdown(
            '<div class="login-footer">Masuk atau daftar untuk melanjutkan.</div>',
            unsafe_allow_html=True,
        )
