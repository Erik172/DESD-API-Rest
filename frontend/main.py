import streamlit as st
import pandas as pd

st.page_link('main.py', label='Home', icon='🏠', disabled=True)
st.page_link('pages/trabajos.py', label='Trabajos', icon='📂', help='Pagina donde se encuentra todos los reportes de todos los modelos corridos')
st.page_link('pages/auditoria.py', label='Auditoría', icon='🔍', disabled=True)
st.page_link('pages/tilde.py', label='TilDe (Tilted Detection) Detección de inclinación', icon='📐', help='Modelo de Detección de inclinación', disabled=False)
st.page_link('pages/rode.py', label='RoDe (Rotation Detection) Detección de rotación', icon='🔄', help='Modelo de Deteccion de Rotacion')
st.page_link('pages/cude.py', label='CuDe (Cut Detection) Detección de cortes de información', icon='✂️', disabled=True)
st.page_link('pages/dude.py', label='DuDe (Duplicate Detection) Detección de duplicados', icon='2️⃣', help='Modelo de Detección de duplicados')

models = pd.DataFrame({
    'Modelo': ['TilDe', 'RoDe', 'CuDe'],
    'Versión': ['v1', 'v1', 'v1'],
    'Descripción': ['Detección de inclinación V1', 'Detección de rotación V1', 'Detección de cortes de información V1'],
    'accuracy': ['97%', '99%', '-'],
    'precision': ['98%', '99%', '-'],
})

st.subheader("Tabla de modelos y métricas")

st.table(models)
st.caption("Tabla de modelos y métricas")