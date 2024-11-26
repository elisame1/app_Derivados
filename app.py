from util.functions import (
    get_news_for_ticker, 
    risk_calculator_tab, 
    create_interactive_visualizations, 
    display_option_price_factors, 
    create_risk_matrix,
    show_risk_explanation
)
from util.risk_matrix import calculate_impact_score, calculate_probability_score, create_matrix
from util.anthropic_util import display_chat_interface
from util.finviz import INDUSTRIES, get_finviz_dataframe

import streamlit as st
import yfinance as yf  # Necesitas instalar esto: pip install yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.graph_objects as go

from datetime import datetime, timedelta


st.title("📈 Guía de derivados para principantes")
st.markdown("### Tu compañero para aprender a invertir en derivados")

# Crear las pestañas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📚 Educación", 
    "📊 Análisis de Datos", 
    "🎯 Herramientas de Decisión",
    "📄 Noticias",
    "💬 Consulta la IA",
    "🔍 Análisis de Riesgo"
])

#1er TAB --------------------------------------------------------------------------------------------------------------



# Estilos CSS adaptables
css = """
<style>
    /* Estilo para el contenedor de navegación */
    .nav-container {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1.2rem;
        border-radius: 5px;
        margin-top: 0;
        min-height: 300px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    /* Estilo para los expanders */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
        margin-bottom: 0.5rem;
    }
    
    /* Estilo para las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Ajuste para el radio button */
    .st-bw {
        color: inherit;
    }
</style>
"""

# Contenido para la pestaña Educativa
with tab1:
    # Inyectar CSS
    st.markdown(css, unsafe_allow_html=True)
    
    # Crear el layout con columnas
    col_nav, col_content = st.columns([1.5, 4])
    
    # Navegación en la columna izquierda
    with col_nav:
        st.markdown("### 📚 Contenido")  # Título directo sin contenedor adicional
        #st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        current_section = st.radio(
            "",
            options=[
                "Conceptos Básicos",
                "Tipos de Instrumentos",
                "Matriz de Riesgo",
                "Factores de Precio"
            ],
            label_visibility="collapsed",
            key="nav_radio"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Contenido en la columna derecha
    with col_content:
        if current_section == "Conceptos Básicos":
            st.subheader("📖 Conceptos Básicos")
            
            with st.expander("📚 Conceptos Esenciales"):
                st.write("""
                • **Derivado Financiero**: Contrato cuyo valor se deriva de otro activo subyacente (acciones, bonos, materias primas, divisas)
                
                • **Activo Subyacente**: El activo base del cual el derivado obtiene su valor
                
                • **Fecha de Vencimiento**: Momento en que el contrato expira y se debe ejecutar
                
                • **Precio de Ejercicio (Strike Price)**: Precio acordado para la operación futura
                """)

            with st.expander("📊 Tipos de Derivados"):
                st.write("""
                • **Futuros**: Contratos que obligan a comprar/vender un activo en fecha futura a precio establecido        
                • **Forwards**: Similar a futuros pero personalizado y negociado fuera de bolsa  
                • **Opciones**: Derecho (no obligación) de comprar/vender a precio establecido

                    • Call: Derecho a comprar
                    • Put: Derecho a vender
                         
                • **Swaps**: Intercambio de flujos financieros entre partes
                """)
            
            with st.expander("⚠️ Conceptos de Riesgo"):
                st.write("""
                • **Prima**: Costo inicial de comprar una opción
                         
                • **Apalancamiento**: Capacidad de controlar mayor cantidad de activos con menor capital
                         
                • **Volatilidad**: Medida de variación del precio del activo subyacente
                         
                • **Posición**:

                    Larga Beneficio cuando sube el precio
                    Corta Beneficio cuando baja el precio
                """)
            
            with st.expander("🎯 Estrategias Básicas"):
                st.write("""
                • **Cobertura (Hedging)**: Protección contra movimientos adversos del mercado
                         
                • **Especulación**: Búsqueda de beneficio por movimientos del mercado
                         
                • **Arbitraje**: Aprovechamiento de diferencias de precios en distintos mercados


                """)
            with st.expander("💹 Valoración"):
                st.write("""
                • **Valor Intrínseco**: Beneficio inmediato si se ejerciera la opción
                        
                • **Valor Temporal**: Valor adicional por tiempo hasta vencimiento
                
                • **Factores Clave**:

                    • Precio del subyacente
                        
                    • Tiempo hasta vencimiento
                        
                    • Volatilidad
                        
                    • Tasas de interés
                """)
                
        # [El resto del código sigue igual...]
        elif current_section == "Tipos de Instrumentos":
            st.subheader("🔧 Tipos de Instrumentos")
            instrument_tab1, instrument_tab2, instrument_tab3 = st.tabs([
                "Opciones 📊", 
                "Futuros 📈", 
                "Forwards 🔄"
            ])
            
            with instrument_tab1:
                st.write("""
                ### Opciones Financieras
                [...]
                """)
                
        elif current_section == "Matriz de Riesgo":
            st.subheader("🎯 Matriz de Riesgo - Derivados Financieros")
            create_risk_matrix()
            
        elif current_section == "Factores de Precio":
            st.subheader("💰 Los 8 Factores que Afectan el Precio de las Opciones")
            display_option_price_factors()

#2do TAB --------------------------------------------------------------------------------------------------------------

# Contenido para la pestaña de Análisis
with tab2:
    st.header("Análisis de Datos")
    st.markdown("""
    Aquí podrás:
    - Visualizar precios históricos
    - Analizar indicadores técnicos
    - Estudiar la volatilidad
    """)

#MULTISELECT

    # Lista de empresas del S&P 500 con sus tickers e industrias
    sp500_companies = {
        'AAPL': {'name': 'Apple Inc.', 'industry': 'Technology'},
        'MSFT': {'name': 'Microsoft Corporation', 'industry': 'Technology'},
        'AMZN': {'name': 'Amazon.com Inc.', 'industry': 'Consumer Discretionary'},
        'NVDA': {'name': 'NVIDIA Corporation', 'industry': 'Technology'},
        'GOOGL': {'name': 'Alphabet Inc. (Google) Class A', 'industry': 'Technology'},
        'GOOG': {'name': 'Alphabet Inc. (Google) Class C', 'industry': 'Technology'},
        'META': {'name': 'Meta Platforms Inc.', 'industry': 'Communication Services'},
        'BRK.B': {'name': 'Berkshire Hathaway Inc.', 'industry': 'Financials'},
        'TSLA': {'name': 'Tesla Inc.', 'industry': 'Consumer Discretionary'},
        'UNH': {'name': 'UnitedHealth Group Inc.', 'industry': 'Healthcare'},
        'LLY': {'name': 'Eli Lilly and Company', 'industry': 'Healthcare'},
        'JPM': {'name': 'JPMorgan Chase & Co.', 'industry': 'Financials'},
        'V': {'name': 'Visa Inc.', 'industry': 'Financials'},
        'XOM': {'name': 'Exxon Mobil Corporation', 'industry': 'Energy'},
        'AVGO': {'name': 'Broadcom Inc.', 'industry': 'Technology'},
        'PG': {'name': 'Procter & Gamble Company', 'industry': 'Consumer Staples'},
        'MA': {'name': 'Mastercard Incorporated', 'industry': 'Financials'},
        'HD': {'name': 'Home Depot Inc.', 'industry': 'Consumer Discretionary'},
        'CVX': {'name': 'Chevron Corporation', 'industry': 'Energy'},
        'ABBV': {'name': 'AbbVie Inc.', 'industry': 'Healthcare'},
        'MRK': {'name': 'Merck & Co. Inc.', 'industry': 'Healthcare'},
        'PFE': {'name': 'Pfizer Inc.', 'industry': 'Healthcare'},
        'COST': {'name': 'Costco Wholesale Corporation', 'industry': 'Consumer Staples'},
        'WMT': {'name': 'Walmart Inc.', 'industry': 'Consumer Staples'},
        'KO': {'name': 'Coca-Cola Company', 'industry': 'Consumer Staples'}
    }

    # Obtener lista única de industrias
    industries = sorted(list(set(company['industry'] for company in sp500_companies.values())))

    # Multiselect de industrias
    selected_industries = st.multiselect(
        'Selecciona las industrias:',
        options=industries,
        default=industries,  # Por defecto todas las industrias seleccionadas
        key='industry_selector'
    )

    # Filtrar empresas por industrias seleccionadas
    if selected_industries:
        options = [
            f"{ticker} - {data['name']}"
            for ticker, data in sp500_companies.items()
            if data['industry'] in selected_industries
        ]
    else:
        options = []  # Si no hay industrias seleccionadas, no mostrar empresas

    # Crear multiselect para empresas
    selected_companies = st.multiselect(
        'Selecciona las empresas que deseas analizar:',
        options=options,
        default=[],
        key='company_selector'
    )

    # Mostrar empresas seleccionadas
    if selected_companies:
        st.write("### Empresas seleccionadas:")
        for company in selected_companies:
            ticker = company.split(" - ")[0]
            industry = sp500_companies[ticker]['industry']
            st.write(f"{company} ({industry})")
        
        # Extraer solo los tickers de las selecciones
        selected_tickers = [company.split(" - ")[0] for company in selected_companies]
        
        # Guardar los tickers seleccionados en session state para uso posterior
        st.session_state['selected_tickers'] = selected_tickers

    #3er TAB --------------------------------------------------------------------------------------------------------------

    # Contenido para la pestaña de Herramientas
    with tab3:
        st.header("Herramientas de Decisión")
        st.markdown("""
        Herramientas disponibles:
        - Calculadora de riesgo
        - Simulador de escenarios
        - Evaluador de posiciones
        """)

        risk_calculator_tab()

        create_interactive_visualizations()

        
      
#4ta TAB --------------------------------------------------------------------------------------------------------------

# Contenido para la pestaña de Noticias
# Contenido para la pestaña de Noticias

get_news_for_ticker('')

with tab4:
    st.header("📰 Noticias de Mercado")
    
    # Selector de ticker para noticias
    ticker_input = st.text_input("Ingresa el nombre del ticker:", "")
    
    if ticker_input:
        ticker_input = ticker_input.upper()
        with st.spinner(f'Cargando noticias para {ticker_input}...'):
            news_dfs = get_news_for_ticker(ticker_input)
            
            if news_dfs:
                st.success(f"Últimas noticias encontradas para {ticker_input}")

                def display_news_column(df_list, idx):
                    for _, row in df_list[idx].iterrows():
                        if 'thumbnail' in row and row['thumbnail'] and row['thumbnail'].get('resolutions'):
                            # Obtener la primera resolución disponible
                            img_url = row['thumbnail']['resolutions'][0]['url']
                            st.image(img_url, use_column_width=True)
                        else:
                            # Si no hay imagen, mostrar un placeholder
                            st.markdown("🖼️ *No hay imagen disponible*")
                    
                        # Contenedor de la noticia
                        st.markdown(f"""
                        **📑 {row['title']}**

                        **Fuente:** {row['publisher']}  
                        **Fecha:** {row['providerPublishTime'].strftime('%Y-%m-%d %H:%M')}
                        
                        [Leer la noticia completa]({row['link']})
                        """)
                        
                        # Si hay enlaces relacionados
                        if 'relatedTickers' in row and row['relatedTickers']:
                            st.markdown("**Tickers relacionados:** " + ", ".join(row['relatedTickers']))

                        st.divider()

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    display_news_column(news_dfs, 0)

                with col2:
                    display_news_column(news_dfs, 1)

                with col3:
                    display_news_column(news_dfs, 2)

                
                # Mostrar información del ticker

                
                try:
                    ticker = yf.Ticker(ticker_input)
                    info = ticker.info
                    
                    st.markdown("---")
                    st.subheader("📊 Información del Mercado")
                    
                    # Crear columnas para información básica
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Precio Actual",
                            f"${info.get('currentPrice', 'N/A'):,.2f}",
                            f"{info.get('regularMarketChangePercent', 0):.2f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Volumen",
                            f"{info.get('volume', 'N/A'):,}"
                        )
                    
                    with col3:
                        st.metric(
                            "Market Cap",
                            f"${info.get('marketCap', 0)/1e9:.2f}B"
                        )
                        
                    # Información adicional en un expander
                    with st.expander("📈 Más información del ticker"):
                        st.markdown(f"""
                        **Sector:** {info.get('sector', 'N/A')}  
                        **Industria:** {info.get('industry', 'N/A')}  
                        **País:** {info.get('country', 'N/A')}  
                        **Empleados:** {info.get('fullTimeEmployees', 'N/A'):,}  
                        
                        **Descripción del negocio:**  
                        {info.get('longBusinessSummary', 'No hay descripción disponible.')}
                        """)
                        
                except Exception as e:
                    st.info("Ticker no encontrado: verifica el nombre del ticker escrito")
            else:
                st.warning(f"No se encontraron noticias recientes para {ticker_input}")
    else:
        st.info("👆 Ingresa un símbolo de ticker para ver sus noticias relacionadas")
        
    # Disclaimer
    st.markdown("""
    ---
    *Disclaimer: La información mostrada proviene de Yahoo Finance y puede tener un retraso. 
    No debe ser considerada como consejo financiero.*
    """)
#5to tab IA--------------------------------------------------------------------------------------------------------------------------------------------


with tab5:
   display_chat_interface()



#6to tab ANÁLISIS DE RIESGO----------------------------------------------------------------------------------------------------------------------------------------------------------
    # File uploader
with tab6:
    finviz_data = get_finviz_dataframe(filtros='')
    finviz_data.info()

    selected_pill = st.pills(
        "Industria",
        options=INDUSTRIES,
        selection_mode="single"
    )

    if selected_pill:
        finviz_data_filtered = finviz_data[0:0]

        # Multiselect de tickers
        selected_tickers = st.multiselect(
            'Selecciona los Tickers (ej. AAPL):',
            options=finviz_data[finviz_data['Sector'] == selected_pill][['Company']].to_dict(orient="index").keys(),
            placeholder='Buscar ticker'
        )

        if selected_pill != 'All' and selected_tickers:
            finviz_data_filtered = finviz_data[finviz_data['Sector'] == selected_pill].loc[selected_tickers]

        # st.dataframe(finviz_data_filtered, use_container_width=True)
        
        # MATRIZ RIESGO ------------------------------------------------------------------------------------------
        try:
            # Display risk matrix
            fig = create_matrix(finviz_data_filtered)
            st.plotly_chart(fig)
            
            # Display risk categories
            st.subheader("Categorización de Riesgo por Ticker")
            
            risk_df = pd.DataFrame({
                'Company': finviz_data_filtered['Company'],
                'Impact Score': calculate_impact_score(finviz_data_filtered),
                'Probability Score': calculate_probability_score(finviz_data_filtered)
            })
            
            def categorize_risk(row):
                if row['Impact Score'] > 0.5 and row['Probability Score'] > 0.5:
                    return "Alto riesgo"
                elif row['Impact Score'] > 0.5:
                    return "Riesgo de impacto"
                elif row['Probability Score'] > 0.5:
                    return "Riesgo de evento adverso"
                else:
                    return "Bajo riesgo"
            
            risk_df['Risk Category'] = risk_df.apply(categorize_risk, axis=1)
            st.dataframe(risk_df)
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
    
    with st.expander("¿Cómo interpretar la matriz?"):
        st.write(show_risk_explanation())

