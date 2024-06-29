import requests
import streamlit as st

st.title("Resultados 📁")

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

resultados = requests.get("http://localhost:5000/v1/resultados").json()

for resultado in resultados:
    with st.expander(f"Resultado: **{resultado}**", expanded=False):
        if st.button(f'Cargar datos de exportación para el trabajo {resultado}'):
            data = requests.get(f"http://localhost:5000/v1/export/{resultado}").json()
            st.write(f'Imágenes procesadas: **{data["total"]}**')

            with st.container():
                st.download_button(
                    label="Descargar CSV",
                    data=requests.get(f"http://localhost:5000{data['url']}").content,
                    file_name=f"{resultado}.csv",
                    mime="text/csv"
                )

        if st.button(f"Eliminar Resultado {resultado}"):
            requests.delete(f"http://localhost:5000/v1/resultados/{resultado}")
            requests.delete(f"http://localhost:5000/v1/export/{resultado}")
            st.success(f"Resultado {resultado} eliminado con éxito.")
            st.toast("Resultado eliminado con éxito.", icon="✅")
            st.experimental_rerun()
