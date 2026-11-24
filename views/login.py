import time

import streamlit as st

from core import db

MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCK_SECONDS = 60


def render():
    _, form_column, _ = st.columns([1, 2, 1], gap="large")
    with form_column:
        st.image("assets/sewain_logo_transparent.png", width=180)
        st.markdown(
            '<div class="login-heading">Masuk ke Sewain</div>'
            '<div class="login-subtitle">Sistem Penyewaan Inventaris UKM</div>',
            unsafe_allow_html=True,
        )

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
                st.session_state["pengguna"] = pengguna
                st.session_state.pop("login_failures", None)
                st.session_state.pop("login_locked_until", None)
                st.rerun()

        st.markdown(
            '<div class="login-footer">Akses khusus administrator Sewain.</div>',
            unsafe_allow_html=True,
        )
