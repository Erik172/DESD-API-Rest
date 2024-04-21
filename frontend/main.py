import streamlit as st

st.page_link('main.py', label='Home', icon='🏠', disabled=True)
st.page_link('pages/auditoria.py', label='Auditoría', icon='🔍')
st.page_link('pages/tilde.py', label='TilDe (Tilted Detection)', icon='📐')
st.page_link('pages/rode.py', label='RoDe (Rotation Detection)', icon='🔄')