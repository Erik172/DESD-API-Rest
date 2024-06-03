import streamlit as st

st.page_link('main.py', label='Home', icon='🏠', disabled=True)
st.page_link('pages/auditoria.py', label='Auditoría', icon='🔍', disabled=False)
st.page_link('pages/resultados.py', label='Resultados', icon='📂', help='Pagina donde se encuentra todos los reportes de todos los modelos corridos')