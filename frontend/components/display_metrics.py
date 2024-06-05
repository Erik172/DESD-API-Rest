import streamlit as st

def single_model_metrics(response):
    """
    Display metrics for a single model prediction.

    Args:
        response (dict): The response containing the prediction data.

    Returns:
        None
    """
    prediction, confidence, tiempo = st.columns(3)
    prediction.metric("Predicción", response['data'][0]['name'])
    confidence.metric("Confianza", f"{response['data'][0]['confidence'] * 100} %")
    tiempo.metric("Tiempo", f"{round(response['time'], 2)} s")

def display_multi_metrics(response):
    """
    Display multiple metrics for each file, model, and page in the response.

    Parameters:
    - response (dict): A dictionary containing the response data.

    Returns:
    - None
    """
    for file in response:
        st.header(f'Archivo: {file}')
        for modelname in response[file]:
            st.subheader(modelname)
            for page in response[file][modelname]:
                st.caption(f'Página: {page}')

                prediction, confidence, tiempo = st.columns(3)
                prediction.metric("Predicción", response[file][modelname][page]['prediccion'])
                confidence.metric("Confianza", f"{response[file][modelname][page]['confianza']} %")
                tiempo.metric("Tiempo", f"{round(response[file][modelname][page]['tiempo(s)'], 2)} s") 
            st.divider()      