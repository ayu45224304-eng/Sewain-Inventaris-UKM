import pandas as pd
import streamlit as st

from core import db
from core.utils import PROGRAM_STUDI_PER_JURUSAN, validasi_penyewa
from views.common import header


EDIT_ACTION_KEY = "penyewa_edit_action"
EDITING_ID_KEY = "penyewa_editing_id"
EDIT_DIALOG_KEY = "penyewa_edit_dialog_key"


def _status_data(row):
    fields = ("nama", "no_hp", "email", "jurusan", "prodi")
    return (
        "Lengkap"
        if all(str(row.get(field) or "").strip() for field in fields)
        else "Belum Lengkap"
    )


def _pilih_penyewa_untuk_diedit(penyewa_ids):
    click = st.session_state.get(EDIT_ACTION_KEY)
    if click is None:
        return
    row_index = click["row"]
    if isinstance(row_index, int) and 0 <= row_index < len(penyewa_ids):
        dialog_counter = st.session_state.get("penyewa_edit_dialog_counter", 0) + 1
        st.session_state["penyewa_edit_dialog_counter"] = dialog_counter
        penyewa_id = penyewa_ids[row_index]
        st.session_state[EDITING_ID_KEY] = penyewa_id
        st.session_state[EDIT_DIALOG_KEY] = f"penyewa_edit_{penyewa_id}_{dialog_counter}"


def _tutup_dialog_edit_penyewa():
    st.session_state.pop(EDITING_ID_KEY, None)
    st.session_state.pop(EDIT_DIALOG_KEY, None)


def _render_penyewa_table(rows):
    frame = pd.DataFrame(rows)
    if frame.empty:
        frame = pd.DataFrame(
            columns=[
                "id",
                "NIM",
                "NAMA",
                "JURUSAN",
                "PROGRAM STUDI",
                "NO TELEPON",
                "EMAIL",
                "JUMLAH TRANSAKSI",
                "STATUS DATA",
            ]
        )
    else:
        frame["NIM"] = frame["nim"].fillna("-").replace({"": "-"})
        frame["NAMA"] = frame["nama"].fillna("-").replace({"": "-"})
        frame["JURUSAN"] = frame["jurusan"].fillna("-").replace({"": "-"})
        frame["PROGRAM STUDI"] = frame["prodi"].fillna("-").replace({"": "-"})
        frame["NO TELEPON"] = frame["no_hp"].fillna("-").replace({"": "-"})
        frame["EMAIL"] = frame["email"].fillna("-").replace({"": "-"})
        frame["JUMLAH TRANSAKSI"] = frame["jumlah_transaksi"].fillna(0).astype(int)
        frame["STATUS DATA"] = frame.apply(_status_data, axis=1)
        frame = frame[
            [
                "id",
                "NIM",
                "NAMA",
                "JURUSAN",
                "PROGRAM STUDI",
                "NO TELEPON",
                "EMAIL",
                "JUMLAH TRANSAKSI",
                "STATUS DATA",
            ]
        ]

    frame["EDIT"] = ":material/edit:"
    penyewa_ids = frame.pop("id").tolist()
    st.markdown(
        """
        <style>
        [data-testid="stDataObjectViz"] th,
        div[data-testid="stTable"] th,
        [data-testid="stDataFrame"] [role="columnheader"],
        [data-testid="stDataFrame"] [role="columnheader"] * {
            text-align: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(
        frame,
        column_config={
            "NIM": st.column_config.TextColumn("NIM", alignment="center"),
            "NAMA": st.column_config.TextColumn("NAMA", alignment="left"),
            "JURUSAN": st.column_config.TextColumn("JURUSAN", alignment="left"),
            "PROGRAM STUDI": st.column_config.TextColumn("PROGRAM STUDI", alignment="left"),
            "NO TELEPON": st.column_config.TextColumn("NO TELEPON", alignment="center"),
            "EMAIL": st.column_config.TextColumn("EMAIL", alignment="left"),
            "JUMLAH TRANSAKSI": st.column_config.NumberColumn(
                "JUMLAH TRANSAKSI",
                format="%d",
                alignment="center",
            ),
            "STATUS DATA": st.column_config.TextColumn("STATUS DATA", alignment="center"),
            "EDIT": st.column_config.ButtonColumn(
                "EDIT",
                width="small",
                type="tertiary",
                alignment="center",
                key=EDIT_ACTION_KEY,
                on_click=_pilih_penyewa_untuk_diedit,
                args=(penyewa_ids,),
            ),
        },
        width="stretch",
        hide_index=True,
    )
    return penyewa_ids


@st.dialog(
    "Edit data penyewa",
    width="medium",
    on_dismiss=_tutup_dialog_edit_penyewa,
)
def _edit_penyewa_dialog(penyewa_id, dialog_key):
    _edit_penyewa_dialog_body(penyewa_id, dialog_key)


def _edit_penyewa_dialog_body(penyewa_id, dialog_key):
    penyewa = db.get_penyewa(penyewa_id)
    if penyewa is None:
        st.error("Data penyewa tidak ditemukan.")
        return

    jurusan_options = list(PROGRAM_STUDI_PER_JURUSAN)
    current_jurusan = penyewa.get("jurusan") or ""
    jurusan_key = f"{dialog_key}_jurusan"
    initial_jurusan = current_jurusan if current_jurusan in jurusan_options else None
    st.session_state.setdefault(f"{dialog_key}_nim", penyewa["nim"])
    st.session_state.setdefault(f"{dialog_key}_nama", penyewa.get("nama") or "")
    st.session_state.setdefault(jurusan_key, initial_jurusan)
    st.session_state.setdefault(f"{dialog_key}_no_hp", penyewa.get("no_hp") or "")
    st.session_state.setdefault(f"{dialog_key}_email", penyewa.get("email") or "")

    st.text_input("NIM", disabled=True, key=f"{dialog_key}_nim")
    nama = st.text_input("Nama", key=f"{dialog_key}_nama")
    jurusan = st.selectbox(
        "Jurusan",
        jurusan_options,
        placeholder="Pilih jurusan",
        key=jurusan_key,
    )
    prodi_options = PROGRAM_STUDI_PER_JURUSAN.get(jurusan, [])
    prodi_key = f"{dialog_key}_prodi_{jurusan}"
    if prodi_key not in st.session_state:
        initial_prodi = penyewa.get("prodi") if jurusan == current_jurusan else None
        st.session_state[prodi_key] = (
            initial_prodi
            if initial_prodi in prodi_options
            else (prodi_options[0] if prodi_options else None)
        )
    prodi = st.selectbox(
        "Program studi",
        prodi_options,
        key=prodi_key,
        disabled=not prodi_options,
    )
    no_hp = st.text_input("Nomor telepon", key=f"{dialog_key}_no_hp")
    email = st.text_input("Email", key=f"{dialog_key}_email")
    simpan_col, batal_col = st.columns(2)
    simpan = simpan_col.button("Simpan perubahan", type="primary", key=f"{dialog_key}_save", width="stretch")
    batal = batal_col.button("Batal", key=f"{dialog_key}_cancel", width="stretch")

    if batal:
        _tutup_dialog_edit_penyewa()
        st.rerun()
    if simpan:
        errors = validasi_penyewa(penyewa["nim"], nama, no_hp, email, jurusan, prodi)
        if errors:
            for message in errors:
                st.error(message)
            return
        try:
            db.ubah_penyewa(penyewa_id, nama, no_hp, email, jurusan, prodi)
        except ValueError as error:
            st.error(str(error))
            return
        st.toast("Data penyewa diperbarui.")
        _tutup_dialog_edit_penyewa()
        st.rerun()


def render():
    header(
        "MASTER DATA",
        "Data Penyewa",
        "Kelola data master penyewa sebagai acuan utama untuk seluruh transaksi.",
    )
    keyword = st.text_input("Pencarian", placeholder="Cari nama atau NIM", key="penyewa_search")
    rows = db.list_penyewa(keyword)
    _render_penyewa_table(rows)
    editing_id = st.session_state.get(EDITING_ID_KEY)
    dialog_key = st.session_state.get(EDIT_DIALOG_KEY)
    if editing_id is not None and dialog_key is not None:
        _edit_penyewa_dialog(editing_id, dialog_key)

    st.markdown("### Tambah penyewa")
    form_version = st.session_state.get("penyewa_add_form_version", 0)
    nim_col, nama_col = st.columns(2)
    nim = nim_col.text_input("NIM", key=f"penyewa_tambah_nim_{form_version}")
    nama = nama_col.text_input("Nama", key=f"penyewa_tambah_nama_{form_version}")

    jurusan_col, prodi_col = st.columns(2)
    jurusan_key = f"penyewa_tambah_jurusan_{form_version}"
    jurusan_options = list(PROGRAM_STUDI_PER_JURUSAN)
    jurusan = jurusan_col.selectbox(
        "Jurusan",
        jurusan_options,
        index=0,
        key=jurusan_key,
    )
    prodi_options = PROGRAM_STUDI_PER_JURUSAN[jurusan]
    prodi_key = f"penyewa_tambah_prodi_{form_version}_{jurusan}"
    prodi = prodi_col.selectbox(
        "Program studi",
        prodi_options,
        key=prodi_key,
    )

    no_hp_col, email_col = st.columns(2)
    no_hp = no_hp_col.text_input("Nomor telepon", key=f"penyewa_tambah_no_hp_{form_version}")
    email = email_col.text_input("Email", key=f"penyewa_tambah_email_{form_version}")
    if st.button("Simpan penyewa", key=f"penyewa_tambah_simpan_{form_version}"):
        errors = validasi_penyewa(nim, nama, no_hp, email, jurusan, prodi)
        if errors:
            for message in errors:
                st.error(message)
        else:
            try:
                db.tambah_penyewa(nim, nama, no_hp, email, jurusan, prodi)
            except ValueError as error:
                st.error(str(error))
            else:
                st.session_state["penyewa_add_form_version"] = form_version + 1
                st.toast("Penyewa baru berhasil ditambahkan.")
                st.rerun()

    with st.expander("Hapus penyewa"):
        daftar_hapus = db.query(
            "SELECT id,nim,nama FROM mahasiswa ORDER BY nama COLLATE NOCASE, nim"
        )
        if not daftar_hapus:
            st.info("Belum ada penyewa yang bisa dihapus.")
        else:
            target_hapus = st.selectbox(
                "Pilih penyewa",
                daftar_hapus,
                format_func=lambda row: f"{row['nim']} - {row['nama']}",
                key="penyewa_hapus_selected",
            )
            konfirmasi = st.checkbox(
                "Saya yakin ingin menghapus penyewa ini.",
                key=f"penyewa_hapus_confirm_{target_hapus['id']}",
            )
            if st.button(
                "Hapus penyewa",
                disabled=not konfirmasi,
                key=f"penyewa_hapus_button_{target_hapus['id']}",
            ):
                try:
                    db.hapus_penyewa(target_hapus["id"])
                except ValueError as error:
                    st.error(str(error))
                else:
                    st.toast("Penyewa berhasil dihapus.")
                    st.rerun()
