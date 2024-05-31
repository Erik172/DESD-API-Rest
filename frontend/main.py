import streamlit as st

st.page_link('main.py', label='Home', icon='🏠', disabled=True)
st.page_link('pages/Resultados.py', label='Resultados', icon='📂', help='Pagina donde se encuentra todos los resultados de todos los modelos corridos')
st.page_link('pages/auditoria.py', label='Auditoría', icon='🔍', disabled=True)
st.page_link('pages/tilde.py', label='TilDe (Tilted Detection) Detección de inclinación', icon='📐', help='Modelo de Detección de inclinación', disabled=False)
st.page_link('pages/rode.py', label='RoDe (Rotation Detection) Detección de rotación', icon='🔄', help='Modelo de Deteccion de Rotacion')
# st.page_link('pages/cude.py', label='CuDe (Cut Detection) Detección de cortes de información', icon='✂️', disabled=True)
st.page_link('pages/dude.py', label='DuDe (Duplicate Detection) Detección de duplicados', icon='2️⃣', help='Modelo de Detección de duplicados')

st.header('Modelos listos para producción')
st.success("Versiones estable para uso en producción", icon="🚀")
st.page_link('pages/rode.py', label='RoDe (Rotation Detection) Detección de rotación', icon='🔄', help='Modelo de Deteccion de Rotacion')
st.page_link('pages/tilde.py', label='TilDe (Tilted Detection) Detección de inclinación', icon='📐', help='Modelo de Detección de inclinación', disabled=False)