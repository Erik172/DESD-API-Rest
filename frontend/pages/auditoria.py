from pdf2image import convert_from_bytes
import streamlit as st
import pandas as pd
import requests
import os

API_URL_BASE = "http://localhost:5000/audit"

st.set_page_config(
    page_title="Auditoría",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Auditoría 🔍")
st.markdown("Esta página es para auditar las imágenes y archivos PDF. Puede subir imágenes o archivos PDF para obtener las predicciones.")
    
show_image = st.checkbox("Mostrar previzualización de la imagen", value=False)
uploaded_file = st.file_uploader("Subir Imagenes", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Subir Archivos PDF", type=["pdf"], accept_multiple_files=True)

st.caption("Resultados de imagenes con problemas")
placeholder_bad = st.empty()
st.divider()

st.caption("Resultados de imagenes sin problemas")
placeholder_good = st.empty()
st.divider()

st.caption("Todos los resultados")
placeholder_all = st.empty()
st.divider()

dataframe = pd.DataFrame(columns=["archivo", "inclinado", "confianza inclinacion", "rotado", "confianza rotacion", "cortado", "confianza corte"])
bad_dataframe = pd.DataFrame(columns=["archivo", "inclinado", "confianza inclinacion", "rotado", "confianza rotacion", "cortado", "confianza corte"])
good_dataframe = pd.DataFrame(columns=["archivo", "inclinado", "confianza inclinacion", "rotado", "confianza rotacion", "cortado", "confianza corte"])

with st.container():
    placeholder_all.dataframe(dataframe) 
    placeholder_bad.dataframe(bad_dataframe)
    placeholder_good.dataframe(good_dataframe)   


def process_uploaded_images(uploaded_file, show_image):
    global dataframe
    global bad_dataframe
    global good_dataframe
    
    with st.spinner("Procesando..."):
        for file in uploaded_file:
            image = file.read()
            response = requests.post(API_URL_BASE, files={"image": image})
            response = response.json()

            # change names to spanish
            response['tilde']['name'] = "inclinado" if response['tilde']['name'] == "tilted" else "no inclinado"
            response['rode']['name'] = "rotado" if response['rode']['name'] == "rotated" else "no rotado"
            response['cude']['name'] = "con corte informacion" if response['cude']['name'] == "cut" else "sin corte informacion"

            st.caption(file.name)  

            tilted, tilded_confidence = st.columns(2)
            tilted.metric("Inclinado", response['tilde']['name'])
            tilded_confidence.metric("Confianza", f"{response['tilde']['confidence'] * 100} %")

            rotated, rotated_confidence = st.columns(2)
            rotated.metric("Rotado", response['rode']['name'])
            rotated_confidence.metric("Confianza", f"{response['rode']['confidence'] * 100} %")

            cut, cut_confidence = st.columns(2)
            cut.metric("Cortado", response['cude']['name'])
            cut_confidence.metric("Confianza", f"{response['cude']['confidence'] * 100} %")

            data = {
                "archivo": [file.name],
                "inclinado": [response['tilde']['name']],
                "confianza inclinacion": [response['tilde']['confidence'] * 100],
                "rotado": [response['rode']['name']],
                "confianza rotacion": [response['rode']['confidence'] * 100],
                "cortado": [response['cude']['name']],
                "confianza corte": [response['cude']['confidence'] * 100]
            }

            dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

            if response['tilde']['name'] == "inclinado":
                st.error(f':warning: La imagen "**{file.name}**" está inclinada.')

            if response['rode']['name'] == "rotado":
                st.error(f':warning: La imagen "**{file.name}**" está rotada.')

            if response['cude']['name'] == "con corte informacion":
                st.error(f':warning: La imagen "**{file.name}**" tiene cortes de información.')

            if response['tilde']['name'] == "inclinado" or response['rode']['name'] == "rotado" or response['cude']['name'] == "con corte informacion":
                bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
            else:
                good_dataframe = pd.concat([good_dataframe, pd.DataFrame(data)], ignore_index=True)


            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")

            st.divider()
            placeholder_all.dataframe(dataframe)
            placeholder_bad.dataframe(bad_dataframe)
            placeholder_good.dataframe(good_dataframe)

        if dataframe.shape[0] > 0:
            with st.container():
                st.dataframe(dataframe)

def process_pdf_file(uploaded_file, show_image):
    global dataframe
    global bad_dataframe
    global good_dataframe

    with st.spinner("Procesando..."):
        for pdf in uploaded_file:
            images = convert_from_bytes(pdf.read())
            for i, image in enumerate(images):
                image.save(f"temp/temp_{i}.jpg")
                image_path = f"temp/temp_{i}.jpg"
                image = open(f"temp/temp_{i}.jpg", "rb")

                response = requests.post(API_URL_BASE, files={"image": image})
                response = response.json()

                # change names to spanish
                response['tilde']['name'] = "inclinado" if response['tilde']['name'] == "tilted" else "no inclinado"
                response['rode']['name'] = "rotado" if response['rode']['name'] == "rotated" else "no rotado"
                # response['cude']['name'] = "con corte informacion" if response['cude']['name'] == "cut" else "sin corte informacion"

                st.caption(f"Pagina {i + 1} del PDF {pdf.name}")

                tilted, tilded_confidence = st.columns(2)
                tilted.metric("Inclinado", response['tilde']['name'])
                tilded_confidence.metric("Confianza", f"{response['tilde']['confidence'] * 100} %")

                rotated, rotated_confidence = st.columns(2)
                rotated.metric("Rotado", response['rode']['name'])
                rotated_confidence.metric("Confianza", f"{response['rode']['confidence'] * 100} %")

                cut, cut_confidence = st.columns(2)
                cut.metric("Cortado", response['cude']['name'])
                cut_confidence.metric("Confianza", f"{response['cude']['confidence'] * 100} %")

                data = {
                    "archivo": [pdf.name],
                    "pagina": [f'Pagina {i + 1}'],
                    "inclinado": [response['tilde']['name']],
                    "confianza inclinacion": [response['tilde']['confidence'] * 100],
                    "rotado": [response['rode']['name']],
                    "confianza rotacion": [response['rode']['confidence'] * 100],
                    "cortado": [response['cude']['name']],
                    "confianza corte": [response['cude']['confidence'] * 100]
                }

                dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

                if response['tilde']['name'] == "inclinado":
                    st.error(f':warning: La Página **{i + 1}** en el PDF "**{pdf.name}**" está inclinada.')

                if response['rode']['name'] == "rotado":
                    st.error(f':warning: La Página **{i + 1}** en el PDF "**{pdf.name}**" está rotada.')

                if response['cude']['name'] == "con corte informacion":
                    st.error(f':warning: La Página **{i + 1}** en el PDF "**{pdf.name}**" tiene cortes de información.')

                if response['tilde']['name'] == "inclinado" or response['rode']['name'] == "rotado" or response['cude']['name'] == "con corte informacion":
                    bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
                else:
                    good_dataframe = pd.concat([good_dataframe, pd.DataFrame(data)], ignore_index=True)

                if show_image:
                    st.image(image_path, use_column_width=True, caption="Uploaded Image", output_format="JPEG")

                try:
                    os.remove(f"temp/temp_{i}.jpg")
                except PermissionError:
                    print("PermissionError: Unable to delete the temporary file.")

                st.divider()
                placeholder_all.dataframe(dataframe)
                placeholder_bad.dataframe(bad_dataframe)
                placeholder_good.dataframe(good_dataframe)

        if dataframe.shape[0] > 0:
            with st.container():
                st.dataframe(dataframe)

def main():
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image)
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image)

if __name__ == "__main__":
    main()