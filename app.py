import streamlit as st
import pandas as pd
import libreria_funciones as lf
import librería_clases as lc

st.title("Proyecto final UCG")

st.sidebar.title("Parámetros")

st.sidebar.image("Python_logo.png")


modulo = st.sidebar.selectbox("Seleccione un módulo", ["Módulo 1", "Módulo 2", "Módulo 3"] )

if modulo == "Módulo 1":

    uploaded_files = st.file_uploader(
        "Upload data", accept_multiple_files=True, type="csv"
    )
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.write(df)

elif modulo == "Módulo 2":

    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

    with tab1:
        st.header("Tab 1")
        st.write("Contenido del Tab 1")

        col1, col2, col3 = st.columns(3)

        with col1:

            monto = st.number_input("Ingrese el monto:", min_value = 0 , max_value = 10000, value=1000)
        with col2:
            interes = st.number_input("Ingrese el interes:",min_value = 0.0 , max_value = 1.0, value=0.10)
            anios = st.number_input("Ingrese el número de años del prestamo:",value=1)
            
        with col3:
             numero_pagos = st.number_input("Ingrese el número pagos anuales:" , value = 12)



    with tab2:
        st.header("Tab 2")
        st.write("Contenido del Tab 2")

        cuota = lf.cuota_prestamo(monto, interes,anios,numero_pagos)
        st.write("Su cuota mensual es: ",cuota)

    with tab3:
        st.header("Tab 3")
        st.write("Contenido del Tab 3") 

    
    


else:
    st.write("Se encuentra en el módulo 3")
