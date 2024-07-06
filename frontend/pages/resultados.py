import requests
import streamlit as st
from datetime import datetime

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

st.title("Resultados 📁")
st.caption("V1.5 - Todo en un solo lugar 📊")

status = requests.get("http://localhost:5000/v2/status").json()
status_ids = [status["result_id"] for status in status]

for item in status:
    item['start_time'] = datetime.strptime(item['start_time'], "%Y-%m-%d %H:%M:%S")  # Ajustar el formato según sea necesario
    item['last_updated'] = datetime.strptime(item['last_updated'], "%Y-%m-%d %H:%M:%S")  # Ajustar el formato según sea necesario
status = sorted(status, key=lambda x: x['start_time'], reverse=True)

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

                total_files, total_time = st.columns(2)
                total_files.write(f"total de archivos procesados: {resultado['total_files']}")
                total_time.write(f"Tiempo transcurrido: {resultado['last_updated'] - resultado['start_time']}")

                modelos = []
                if resultado["tilted"]:
                    modelos.append("📐 Inclinación")
                if resultado["rotation"]:
                    modelos.append("🔄 Rotación")
                if resultado["cut_information"]:
                    modelos.append("✂ Corte información")
                if resultado["duplicate"]:
                    modelos.append("2️⃣ Duplicados")

                st.write(f"Modelos: {', '.join(modelos)}")

                download_btn, delete_btn = st.columns(2)

                if download_btn.button(f"📥 Descargar CSV", use_container_width=True, key=f"descargar_{resultado['result_id']}"):
                    download_csv(resultado['result_id'])  

                if delete_btn.button(f"🗑 Eliminar Resultado", key=f"delete_{resultado['result_id']}", use_container_width=True):
                    requests.delete(f"http://localhost:5000/v2/status/{resultado['result_id']}")
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

                st.write(f"Tiempo transcurrido: {resultado['last_updated'] - resultado['start_time']}")
                
                modelos = []
                if resultado["tilted"]:
                    modelos.append("📐 Inclinación")
                if resultado["rotation"]:
                    modelos.append("🔄 Rotación")
                if resultado["cut_information"]:
                    modelos.append("✂ Corte información")
                if resultado["duplicate"]:
                    modelos.append("2️⃣ Duplicados")

                st.write(f"Modelos: {', '.join(modelos)}")

                if st.button(f"📥 Descargar resultados parciales", help="Descargar resultados parciales en CSV", use_container_width=True, key=f"partial_{resultado['result_id']}"):
                    download_csv(resultado['result_id'])

with failed:
    failed_results = [status for status in status if status["status"] == "failed"]
    if not failed_results:
        st.info("No hay resultados fallidos.")
    else:
        st.write(f'Total de resultados fallidos: {len(failed_results)}')
        
        for resultado in failed_results:
            with st.container(border=True):
                resultado_id, start_time, last_updated = st.columns(3)
                resultado_id.write(f"**{resultado['result_id']}**")
                start_time.caption(f"**Inicio:** {resultado['start_time']}")
                last_updated.caption(f"**Última actualización:** {resultado['last_updated']}")

                st.warning(f"El resultado falló en su procesamiento. archivos procesados: {resultado['files_processed']} de {resultado['total_files']}")

                delete_btn = st.empty()

                if delete_btn.button(f"🗑 Eliminar Resultado", key=f"delete_{resultado['result_id']}", use_container_width=True):
                    requests.delete(f"http://localhost:5000/v2/status/{resultado['result_id']}")
                    requests.delete(f"http://localhost:5000/v1/resultados/{resultado['result_id']}")
                    requests.delete(f"http://localhost:5000/v2/export/{resultado['result_id']}")
                    st.success(f"Resultado {resultado['result_id']} eliminado con éxito.")
                    st.toast("Resultado eliminado con éxito.", icon="✅")
                    st.rerun()

