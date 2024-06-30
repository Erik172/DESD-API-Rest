import streamlit as st

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

st.image("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png", width=120)

st.subheader("DESD - Detección de Errores en Documentos Escaneados")
st.caption("Stable Version")

st.page_link('main.py', label='Home', icon='🏠', disabled=True)
st.page_link('pages/auditoria.py', label='Auditoría', icon='🔍', disabled=False)
st.page_link('pages/duplicidad.py', label='Duplicidad', icon='2️⃣', disabled=False)
st.page_link('pages/resultados.py', label='Resultados', icon='📂', help='Pagina donde se encuentra todos los reportes de todos los modelos corridos')