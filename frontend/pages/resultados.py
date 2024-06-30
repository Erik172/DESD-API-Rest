import requests
import streamlit as st
from datetime import datetime

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

st.title("Resultados 📁")
st.caption("V1.1 Beta - En desarrollo 🚧")

status = requests.get("http://localhost:5000/v2/desd/status").json()
status_ids = [status["result_id"] for status in status]

for item in status:
    item['start_time'] = datetime.strptime(item['start_time'], "%Y-%m-%d %H:%M:%S")  # Ajustar el formato según sea necesario
status = sorted(status, key=lambda x: x['start_time'], reverse=True)

st.subheader("Resultados auditoria")

completed, in_progress, failed = st.tabs(["Completados", "En progreso", "Fallidos"])

@st.experimental_dialog("Generando CSV....")
def download_csv(result_id):
    if st.download_button(
        label="Descargar CSV",
        data=requests.get(f"http://localhost:5000/v2/export/{result_id}").content,
        file_name=f"{result_id}.csv",
        mime="text/csv",
        help="Descargar los resultados completos en formato CSV",
        use_container_width=True
    ): 
        st.toast("Descarga iniciada", icon="📥")

with completed:
    completed_results = [status for status in status if status["status"] == "completed"]
    if not completed_results:
        st.info("No hay resultados completados aún.")
    else:
        st.write(f'Total de resultados: {len(completed_results)}')

        for resultado in completed_results:
            with st.container(border=True):
                resultado_id, start_time, end_time = st.columns(3)
                resultado_id.write(f"**{resultado['result_id']}**")
                start_time.caption(f"**Inicio:** {resultado['start_time']}")
                end_time.caption(f"**Fin:** {resultado['last_updated']}")
                st.write(f"total de archivos procesados: {resultado['total_files']}")

                modelos = []
                if resultado["tilted"]:
                    modelos.append("📐 Inclinación")
                if resultado["rotation"]:
                    modelos.append("🔄 Rotación")
                if resultado["cut_information"]:
                    modelos.append("✂ Corte información")

                st.write(f"Modelos: {', '.join(modelos)}")

                download_btn, delete_btn = st.columns(2)

                if download_btn.button(f"📥 Descargar CSV", use_container_width=True, key=f'descargar_{resultado['result_id']}'):
                    download_csv(resultado['result_id'])  

                if delete_btn.button(f"🗑 Eliminar Resultado", key=f"delete_{resultado['result_id']}", use_container_width=True):
                    requests.delete(f"http://localhost:5000/v2/desd/status/{resultado['result_id']}")
                    requests.delete(f"http://localhost:5000/v1/resultados/{resultado['result_id']}")
                    requests.delete(f"http://localhost:5000/v2/export/{resultado['result_id']}")
                    st.success(f"Resultado {resultado['result_id']} eliminado con éxito.")
                    st.toast("Resultado eliminado con éxito.", icon="✅")
                    st.rerun()

with in_progress:
    in_progress_results = [status for status in status if status["status"] == "in_progress"]
    if not in_progress_results:
        st.info("No hay resultados en progreso.")
    else:
        st.write(f'Total de resultados en progreso: {len(in_progress_results)}')
        
        for resultado in in_progress_results:
            with st.container(border=True):
                resultado_id, start_time, last_updated = st.columns(3)
                resultado_id.write(f"**{resultado['result_id']}**")
                start_time.caption(f"**Inicio:** {resultado['start_time']}")
                last_updated.caption(f"**Última actualización:** {resultado['last_updated']}")

                st.progress(resultado["percentage"] / 100, f'{round(resultado["percentage"], 2)}% - {resultado["files_processed"]}/{resultado["total_files"]} archivos procesados')

                modelos = []
                if resultado["tilted"]:
                    modelos.append("📐 Inclinación")
                if resultado["rotation"]:
                    modelos.append("🔄 Rotación")
                if resultado["cut_information"]:
                    modelos.append("✂ Corte información")

                st.write(f"Modelos: {', '.join(modelos)}")

                if st.button(f"📥 Descargar resultados parciales", help="Descargar resultados parciales en CSV", use_container_width=True):
                    download_csv(resultado['result_id'])

with failed:
    failed_results = [status for status in status if status["status"] == "failed"]
    if not failed_results:
        st.warning("🚧 implemetacion en desarrollo 🚧")
    else:
        st.write(f'Total de resultados: {len(failed_results)}')
        st.warning("🚧 implemetacion en desarrollo 🚧")

st.subheader("Resultados Detección Duplicados")

all_resultados = requests.get("http://localhost:5000/v1/resultados").json()
other_resultados = []

for item in all_resultados:
    if item not in status_ids:
        other_resultados.append(item)

if not other_resultados:
    st.info("No hay resultados de detección de duplicados aún.")
else:
    st.write(f'Total de resultados: {len(other_resultados)}')

    for resultado in other_resultados:
        with st.container(border=True):
            st.write(f"**{resultado}**")

            download_btn, delete_btn = st.columns(2)

            if download_btn.button(f"📥 Descargar CSV", help="Descargar los resultados completos en formato CSV", use_container_width=True, key=f"download_{resultado}"):
                download_csv(resultado)

            if delete_btn.button(f"🗑 Eliminar Resultado", key=f"delete_{resultado}", use_container_width=True):
                    requests.delete(f"http://localhost:5000/v2/desd/status/{resultado}")
                    requests.delete(f"http://localhost:5000/v1/resultados/{resultado}")
                    requests.delete(f"http://localhost:5000/v2/export/{resultado}")
                    st.success(f"Resultado {resultado} eliminado con éxito.")
                    st.toast("Resultado eliminado con éxito.", icon="✅")
                    st.rerun()
