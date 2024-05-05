import streamlit as st

def single_model_metrics(response):
    st.progress(response['data'][0]['confidence'], f"{response['data'][0]['name']}, {response['data'][0]['confidence'] * 100} %")
    st.progress(response['data'][1]['confidence'], f"{response['data'][1]['name']}, {response['data'][1]['confidence'] * 100} %")

    prediction, confidence, tiempo = st.columns(3)
    prediction.metric("Predicción", response['data'][0]['name'])
    confidence.metric("Confianza", f"{response['data'][0]['confidence'] * 100} %")
    tiempo.metric("Tiempo", f"{round(response['time'], 2)} s")