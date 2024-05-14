import requests
import streamlit as st
from datetime import datetime

st.title("Trabajos 📁")

works = requests.get("http://localhost:5000/works").json()

# crear por cada work un expander
for work in works:
    with st.expander(f"Trabajo: **{work}**", expanded=False):
        data = requests.get(f"http://localhost:5000/work/{work}/export").json()
        st.caption(f"Fecha de creación del csv: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        st.write(f'Imagénes procesadas: **{data["total"]}**')

        with st.container():
            st.download_button(
                label="Descargar CSV",
                data=requests.get(f"http://localhost:5000{data['url']}").content,
                file_name=f"{work}.csv",
                mime="text/csv"
            )

        if st.button(f"Eliminar trabajo {work}"):
            requests.delete(f"http://localhost:5000/works/{work}")
            requests.delete(f"http://localhost:5000/work/{work}/export")
            st.success(f"Trabajo {work} eliminado con éxito.")
            st.toast("Trabajo eliminado con éxito.", icon="✅")
