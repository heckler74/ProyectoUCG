import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import libreria_funciones as lf
import librería_clases as lc

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Dashboard de Analítica Camaronera",
    page_icon="🦐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para un acabado premium
st.markdown("""
<style>
    /* Estilos generales */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Efecto Glassmorphism en tarjetas de métricas */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 191, 255, 0.15);
        border-color: rgba(56, 189, 248, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Título Principal
st.title("🦐 Panel Analítico del Sector Camaronero")
st.markdown("##### Plataforma interactiva para el monitoreo de crecimiento, alimentación y rentabilidad en piscinas acuícolas.")

# Sidebar de Parámetros y Origen de Datos
st.sidebar.markdown("<div style='text-align: center;'><h2 style='color:#38bdf8;margin-bottom:0;'>Antigravity Analytics</h2><p style='color:#94a3b8;font-size:0.8rem;'>Acuicultura y Ciencia de Datos</p></div>", unsafe_allow_html=True)
st.sidebar.image("Python_logo.png", width=150)
st.sidebar.markdown("---")

st.sidebar.subheader("Origen de Datos")
origen_datos = st.sidebar.radio(
    "Seleccione Fuente de Datos",
    ["Utilizar Datos de Demostración (Simulados)", "Cargar Archivo CSV Propio"]
)

df = None

if origen_datos == "Utilizar Datos de Demostración (Simulados)":
    dias_sim = st.sidebar.slider("Días de cultivo a simular", 30, 120, 90, step=10)
    df = lf.generar_datos_camaronera_simulados(num_dias=dias_sim)
    st.sidebar.success("¡Datos simulados cargados!")
else:
    uploaded_file = st.sidebar.file_uploader(
        "Subir CSV Camaronera", type=["csv"],
        help="El archivo debe contener las columnas: codigo_camaronera, cod_piscina, fecha_muestra, corrida, peso_gramos, consumo_balanceado_kg, num_animales"
    )
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Verificar columnas requeridas
            required_cols = ["codigo_camaronera", "cod_piscina", "fecha_muestra", "corrida", "peso_gramos", "consumo_balanceado_kg", "num_animales"]
            missing_cols = [c for c in required_cols if c not in df.columns]
            if missing_cols:
                st.error(f"Columnas faltantes en el CSV: {', '.join(missing_cols)}")
                df = None
            else:
                st.sidebar.success("¡CSV cargado correctamente!")
        except Exception as e:
            st.error(f"Error al leer el CSV: {str(e)}")
    else:
        st.info("Suba un archivo CSV en la barra lateral para iniciar el análisis, o seleccione la opción de simulación.")

if df is not None:
    # Asegurar tipos de datos adecuados
    df["fecha_muestra"] = pd.to_datetime(df["fecha_muestra"]).dt.strftime("%Y-%m-%d")
    
    # Filtros dinámicos en la barra lateral
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros de Producción")
    
    camaroneras_disponibles = sorted(df["codigo_camaronera"].unique())
    selected_camaronera = st.sidebar.selectbox("Seleccione Camaronera / Finca", camaroneras_disponibles)
    
    # Filtrar piscinas correspondientes a la camaronera seleccionada
    df_cam = df[df["codigo_camaronera"] == selected_camaronera]
    piscinas_disponibles = sorted(df_cam["cod_piscina"].unique())
    selected_piscina = st.sidebar.selectbox("Seleccione Piscina", piscinas_disponibles)
    
    # Filtrar corridas de esa piscina
    df_pis = df_cam[df_cam["cod_piscina"] == selected_piscina]
    corridas_disponibles = sorted(df_pis["corrida"].unique())
    selected_corrida = st.sidebar.selectbox("Seleccione Corrida", corridas_disponibles)
    
    # Filtrar el DataFrame final para el análisis
    df_filtrado = df_pis[df_pis["corrida"] == selected_corrida].sort_values("fecha_muestra")
    
    # Instanciar clases de Negocio (POO)
    camaronera_obj = lc.Camaronera(selected_camaronera)
    camaronera_obj.agregar_datos_desde_dataframe(df)
    piscina_obj = camaronera_obj.obtener_piscina(selected_piscina)
    
    # Obtener resumen por POO
    resumen_piscina = piscina_obj.obtener_resumen()
    
    # Pestañas principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard de KPIs", 
        "🔎 Exploración y EDA", 
        "💰 Simulación Económica",
        "🩺 Diagnóstico e IA"
    ])
    
    with tab1:
        st.subheader(f"Monitoreo Actual: {selected_camaronera} | {selected_piscina} | {selected_corrida}")
        
        # KPIs en tarjetas
        if "estado" not in resumen_piscina:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    label="Peso Promedio Actual", 
                    value=f"{resumen_piscina['peso_actual_g']} g",
                    delta=f"+{round(piscina_obj.adg_promedio() * 7, 2)} g / semana"
                )
            with col2:
                st.metric(
                    label="Biomasa Estimada", 
                    value=f"{resumen_piscina['biomasa_actual_kg']:,} kg",
                    delta=f"Población: {resumen_piscina['poblacion_estimada']:,} animales"
                )
            with col3:
                st.metric(
                    label="FCR (Eficiencia Alimenticia)", 
                    value=f"{resumen_piscina['fcr_actual']}",
                    delta="Objetivo comercial: 1.2 - 1.5",
                    delta_color="off"
                )
            
            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric(
                    label="Alimento Acumulado", 
                    value=f"{resumen_piscina['alimento_acumulado_kg']:,} kg",
                    delta=f"Sacos: {round(resumen_piscina['alimento_acumulado_kg']/50, 1):,}"
                )
            with col5:
                st.metric(
                    label="Supervivencia Acumulada", 
                    value=f"{resumen_piscina['supervivencia_pct']}%",
                    delta=f"Sembrado: {piscina_obj.poblacion_inicial:,} cam."
                )
            with col6:
                st.metric(
                    label="Crecimiento Diario (ADG)", 
                    value=f"{resumen_piscina['adg_promedio_g_dia']} g/día"
                )
        else:
            st.warning("No hay suficientes datos de muestra registrados en esta piscina para calcular los indicadores.")
            
        st.markdown("---")
        st.subheader("Gráficas de Producción")
        
        # Gráfico 1: Curva de crecimiento vs Referencia Comercial
        df_filtrado = df_filtrado.reset_index(drop=True)
        df_filtrado["dias_cultivo"] = df_filtrado.index + 1
        
        # Curva de referencia logística comercial
        w_ref_max = 22.0
        k_ref = 0.065
        t50_ref = 40.0
        df_filtrado["peso_referencia_bio"] = w_ref_max / (1.0 + np.exp(-k_ref * (df_filtrado["dias_cultivo"] - t50_ref)))
        
        fig_crec = go.Figure()
        fig_crec.add_trace(go.Scatter(
            x=df_filtrado["fecha_muestra"], 
            y=df_filtrado["peso_gramos"], 
            mode='lines+markers', 
            name='Peso Promedio Observado (g)',
            line=dict(color='#0ea5e9', width=3),
            marker=dict(size=6)
        ))
        fig_crec.add_trace(go.Scatter(
            x=df_filtrado["fecha_muestra"], 
            y=df_filtrado["peso_referencia_bio"], 
            mode='lines', 
            name='Estándar de Crecimiento Comercial (g)',
            line=dict(color='#64748b', width=2, dash='dash')
        ))
        fig_crec.update_layout(
            title='Curva de Crecimiento del Camarón (gramos) vs Estándar',
            xaxis_title='Fecha del Muestreo',
            yaxis_title='Peso Promedio (g)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template='plotly_dark'
        )
        st.plotly_chart(fig_crec, use_container_width=True)
        
        # Gráfico 2: Alimento diario consumido y peso acumulado (Eje Y dual)
        fig_alim = go.Figure()
        # Consumo balanceado diario (Barras)
        fig_alim.add_trace(go.Bar(
            x=df_filtrado["fecha_muestra"], 
            y=df_filtrado["consumo_balanceado_kg"],
            name='Consumo Diario (kg)',
            marker_color='#10b981',
            opacity=0.75
        ))
        # Peso en gramos (Línea en eje Y secundario)
        fig_alim.add_trace(go.Scatter(
            x=df_filtrado["fecha_muestra"], 
            y=df_filtrado["peso_gramos"],
            name='Peso Promedio (g)',
            line=dict(color='#f59e0b', width=2.5),
            yaxis='y2'
        ))
        
        fig_alim.update_layout(
            title='Relación de Alimentación Diaria vs Peso Corporal del Camarón',
            xaxis_title='Fecha',
            yaxis=dict(
                title='Consumo de Balanceado (kg)',
                titlefont=dict(color='#10b981'),
                tickfont=dict(color='#10b981')
            ),
            yaxis2=dict(
                title='Peso (g)',
                titlefont=dict(color='#f59e0b'),
                tickfont=dict(color='#f59e0b'),
                overlaying='y',
                side='right'
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template='plotly_dark'
        )
        st.plotly_chart(fig_alim, use_container_width=True)

    with tab2:
        st.subheader("Análisis Exploratorio de Datos (EDA)")
        st.write("Estadísticas y distribución de las variables registradas.")
        
        # Mostrar tabla interactiva
        st.dataframe(df_filtrado[["fecha_muestra", "corrida", "peso_gramos", "consumo_balanceado_kg", "num_animales"]], use_container_width=True)
        
        col_k1, col_k2, col_k3 = st.columns(3)
        with col_k1:
            st.metric("Total Muestras Registradas", len(df_filtrado))
        with col_k2:
            st.metric("Valores Faltantes / Nulos", df_filtrado.isnull().sum().sum())
        with col_k3:
            st.metric("Densidad Población Inicial", f"{piscina_obj.poblacion_inicial:,} cam.")
            
        st.markdown("---")
        
        col_eda1, col_eda2 = st.columns(2)
        
        with col_eda1:
            st.markdown("**Resumen Estadístico Numérico**")
            desc_df = df_filtrado[["peso_gramos", "consumo_balanceado_kg", "num_animales"]].describe()
            st.dataframe(desc_df, use_container_width=True)
            
        with col_eda2:
            st.markdown("**Matriz de Correlación**")
            corr = df_filtrado[["peso_gramos", "consumo_balanceado_kg", "num_animales"]].corr()
            fig_corr = px.imshow(
                corr, 
                text_auto=True, 
                aspect="auto", 
                color_continuous_scale='Blues',
                title="Coeficiente de Correlación de Pearson"
            )
            fig_corr.update_layout(template='plotly_dark')
            st.plotly_chart(fig_corr, use_container_width=True)
            
        # Gráfico de distribución de pesos
        fig_hist = px.histogram(
            df_filtrado, 
            x="peso_gramos", 
            nbins=15, 
            marginal="box",
            title="Distribución de Frecuencia del Peso del Camarón",
            color_discrete_sequence=['#38bdf8']
        )
        fig_hist.update_layout(
            xaxis_title="Peso (gramos)",
            yaxis_title="Cantidad de Muestras",
            template='plotly_dark'
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with tab3:
        st.subheader("Simulación Económica de la Cosecha")
        st.write("Monitoree e interactúe con los parámetros comerciales para proyectar la rentabilidad operativa.")
        
        # Parámetros económicos interactivos
        st.markdown("##### Variables Financieras de Cosecha")
        col_fin1, col_fin2, col_fin3 = st.columns(3)
        with col_fin1:
            precio_venta_lb = st.slider(
                "Precio de Venta ($ por Libra)", 
                1.50, 6.00, 3.20, step=0.10,
                help="Precio comercial de camarón entero por libra en pie de finca."
            )
        with col_fin2:
            costo_saco_balanceado = st.slider(
                "Costo de Alimento Balanceado ($ por Saco 50kg)", 
                25, 75, 42, step=1,
                help="Costo promedio del saco de balanceado de 50 kg."
            )
        with col_fin3:
            costos_fijos_hectarea = st.number_input(
                "Costos Adicionales de la Piscina ($)", 
                min_value=0, max_value=25000, value=3500, step=100,
                help="Costos adicionales (electricidad, mano de obra, insumos químicos, etc.)."
            )
        
        # Cálculos financieros (1 Libra = 453.592 gramos)
        precio_venta_kg = precio_venta_lb / 0.453592
        
        biomasa_final_kg = resumen_piscina["biomasa_actual_kg"]
        alimento_final_kg = resumen_piscina["alimento_acumulado_kg"]
        sacos_consumidos = alimento_final_kg / 50.0
        
        ingreso_bruto = biomasa_final_kg * precio_venta_kg
        costo_alimento = sacos_consumidos * costo_saco_balanceado
        utilidad_operativa = ingreso_bruto - costo_alimento - costos_fijos_hectarea
        margen_utilidad = (utilidad_operativa / ingreso_bruto * 100) if ingreso_bruto > 0 else 0.0
        
        st.markdown("---")
        st.markdown("#### 📋 Resultados Proyectados de Cosecha")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("Ingreso Bruto Estimado", f"${ingreso_bruto:,.2f}")
        with col_res2:
            st.metric("Costo Total en Alimentación", f"${costo_alimento:,.2f}", delta=f"{round(sacos_consumidos, 1)} sacos")
        with col_res3:
            color_flag = "normal" if utilidad_operativa > 0 else "inverse"
            st.metric("Utilidad Operativa Proyectada", f"${utilidad_operativa:,.2f}", delta=f"{round(margen_utilidad, 1)}% Margen", delta_color=color_flag)
            
        # Gráfico de pastel de estructura de costos vs utilidad
        costo_otros = costos_fijos_hectarea
        val_utilidad = max(0.0, utilidad_operativa)
        
        labels = ['Costo Alimento', 'Costos Operativos Adicionales', 'Utilidad Proyectada']
        values = [costo_alimento, costo_otros, val_utilidad]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.3,
            marker=dict(colors=['#ef4444', '#f59e0b', '#10b981'])
        )])
        fig_pie.update_layout(
            title="Estructura Económica Proyectada",
            template='plotly_dark'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Exportar datos
        st.markdown("##### Descargar Resultados Financieros")
        export_df = pd.DataFrame([{
            "Camaronera": selected_camaronera,
            "Piscina": selected_piscina,
            "Corrida": selected_corrida,
            "Biomasa Cosechada (kg)": round(biomasa_final_kg, 2),
            "FCR": round(resumen_piscina["fcr_actual"], 2),
            "Supervivencia (%)": round(resumen_piscina["supervivencia_pct"], 2),
            "Ingreso Bruto ($)": round(ingreso_bruto, 2),
            "Costo Alimentacion ($)": round(costo_alimento, 2),
            "Costos Operativos ($)": round(costos_fijos_hectarea, 2),
            "Utilidad Estimada ($)": round(utilidad_operativa, 2)
        }])
        
        csv = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar Reporte de Cosecha en CSV",
            data=csv,
            file_name=f"reporte_cosecha_{selected_piscina}.csv",
            mime="text/csv"
        )

    with tab4:
        st.subheader("🩺 Diagnóstico Técnico y Alertas de Gestión")
        st.write("Análisis lógico automatizado basado en los estándares productivos de la acuicultura.")
        
        fcr = resumen_piscina["fcr_actual"]
        supervivencia = resumen_piscina["supervivencia_pct"]
        adg = resumen_piscina["adg_promedio_g_dia"]
        
        alertas = []
        
        # Diagnóstico de FCR
        if fcr > 1.7:
            alertas.append({
                "tipo": "WARNING",
                "variable": "Factor de Conversión Alimenticia (FCR) Elevado",
                "valor": f"{fcr}",
                "mensaje": "El FCR se encuentra por encima del rango óptimo comercial (1.2 - 1.5). Esto indica suboptimización en la dosificación de alimento, desperdicio por mallas dañadas o mortalidad sumergida no contabilizada. Revise la frecuencia de alimentación y realice inspecciones de fondo en la piscina."
            })
        elif fcr < 1.1:
            alertas.append({
                "tipo": "SUCCESS",
                "variable": "Eficiencia Alimenticia Sobresaliente",
                "valor": f"{fcr}",
                "mensaje": "El factor de conversión alimenticia es excepcionalmente bajo. El camarón está asimilando los nutrientes de forma sumamente eficiente, lo cual reduce significativamente los costos de alimentación."
            })
        else:
            alertas.append({
                "tipo": "NOTE",
                "variable": "Factor de Conversión Alimenticia (FCR) Estable",
                "valor": f"{fcr}",
                "mensaje": "El FCR está dentro del rango comercialmente aceptable. Continúe aplicando las tablas de alimentación basadas en temperatura y muestreo."
            })
            
        # Diagnóstico de Supervivencia
        if supervivencia < 70.0:
            alertas.append({
                "tipo": "CAUTION",
                "variable": "Alerta Crítica de Supervivencia",
                "valor": f"{supervivencia}%",
                "mensaje": "La supervivencia ha caído por debajo del umbral de seguridad comercial del 70%. Existe un riesgo de mortalidad masiva. Se aconseja realizar muestreos urgentes de oxígeno disuelto en horas críticas (madrugada), verificar pH, sulfuros en el fondo y recolectar muestras para análisis patológicos."
            })
        elif supervivencia >= 85.0:
            alertas.append({
                "tipo": "SUCCESS",
                "variable": "Supervivencia de Población Excelente",
                "valor": f"{supervivencia}%",
                "mensaje": "La supervivencia acumulada se mantiene en niveles excelentes. El manejo físico-químico del agua y del suelo de la piscina está siendo ejecutado correctamente."
            })
        else:
            alertas.append({
                "tipo": "NOTE",
                "variable": "Supervivencia Aceptable",
                "valor": f"{supervivencia}%",
                "mensaje": "La supervivencia acumulada se mantiene dentro de los rangos comerciales normales. Mantenga las rutinas de sifoneo de fondo y recambios de agua programados."
            })
            
        # Diagnóstico de Crecimiento (ADG)
        if adg < 0.16:
            alertas.append({
                "tipo": "WARNING",
                "variable": "Crecimiento Lento (ADG)",
                "valor": f"{adg} g/día",
                "mensaje": "El Incremento de Peso Diario (ADG) promedio está por debajo del estándar comercial (0.20 g/día). Esto puede deberse a bajas temperaturas del agua (menores a 24°C), baja calidad proteica en el alimento, o presencia de microorganismos que ralentizan el desarrollo."
            })
        elif adg >= 0.22:
            alertas.append({
                "tipo": "SUCCESS",
                "variable": "Crecimiento Acelerado (ADG)",
                "valor": f"{adg} g/día",
                "mensaje": "Crecimiento rápido por encima del promedio comercial. La piscina alcanzará su peso de mercado anticipadamente, disminuyendo los riesgos de exposición y optimizando los costos fijos."
            })
        else:
            alertas.append({
                "tipo": "NOTE",
                "variable": "Crecimiento y Ganancia de Peso Estable",
                "valor": f"{adg} g/día",
                "mensaje": "El camarón muestra un crecimiento estable y dentro de la planificación comercial."
            })
            
        # Mostrar Alertas
        st.markdown("#### 🔍 Diagnóstico Automatizado de Campo")
        
        for alerta in alertas:
            if alerta["tipo"] == "SUCCESS":
                st.success(f"**🟢 {alerta['variable']}: {alerta['valor']}**\n\n{alerta['mensaje']}")
            elif alerta["tipo"] == "NOTE":
                st.info(f"**🔵 {alerta['variable']}: {alerta['valor']}**\n\n{alerta['mensaje']}")
            elif alerta["tipo"] == "WARNING":
                st.warning(f"**🟡 {alerta['variable']}: {alerta['valor']}**\n\n{alerta['mensaje']}")
            elif alerta["tipo"] == "CAUTION":
                st.error(f"**🔴 {alerta['variable']}: {alerta['valor']}**\n\n{alerta['mensaje']}")
