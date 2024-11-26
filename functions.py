import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import yfinance as yf  # Necesitas instalar esto: pip install yfinance
from datetime import datetime, timedelta

from scipy.stats import norm
import plotly.graph_objects as go

from scipy.stats import norm
import plotly.express as px



#1er tab ---------------------------------------------------------------------------------------------------------------------------------------------------------------------


#         DESCRIPCION DE OPCIONES EN TIPOS DE INSTRUMENTOS - EDUCACIÓN

def options_tab():
    st.markdown("""
    # ¡Bienvenido al mundo de las Opciones! 🎯
    """)

    # Explicación inicial amigable
    st.markdown("""
    ¡Imaginemos que eres todo un experto en predecir el precio de las acciones de Apple! 🍎

    Las opciones son como un 'seguro' para el mercado de valores - te dan el derecho (pero no la obligación) 
    de comprar o vender algo en el futuro a un precio que acordamos hoy.
    """)

    # Crear ejemplo con un callout box
    st.info("""
    ### Veamos un ejemplo real:
    - Apple está en $100 hoy
    - Tienes un presentimiento de que subirá en los próximos meses
    - Puedes comprar una Call (derecho a comprar) con strike de $110
    - Solo te cuesta $5 (la prima) ¡como pagar un seguro!
    """)

    # Escenarios posibles
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✨ Si Apple sube a $130:
        ¡Genial! Puedes comprar a $110 y vender a $130
        
        **Tu ganancia:** $15 ($130 - $110 - $5 de prima)
        """)
    
    with col2:
        st.error("""
        ### ❌ Si Apple baja a $90:
        No pasa nada, solo pierdes los $5 de la prima
        
        Es como cuando no usas el seguro de tu coche, solo perdiste la prima
        """)

    # Sección de gráficos de payoff
    st.markdown("## 📈 Diagramas de Payoff")
    
    tabs_payoff = st.tabs(["Comprar Call", "Vender Call", "Comprar Put", "Vender Put"])
    
    with tabs_payoff[0]:
        st.markdown("### Comprar Call - Estrategia Alcista 📈")
        # Aquí insertaríamos el SVG de Comprar Call
        st.markdown("""
        - **Estrategia:** Apuestas a que el precio subirá
        - **Ganancia máxima:** Ilimitada
        - **Pérdida máxima:** Prima pagada ($5)
        - **Punto de equilibrio:** Strike + Prima
        """)

    with tabs_payoff[1]:
        st.markdown("### Vender Call - Estrategia Bajista/Neutral 📉")
        # Aquí insertaríamos el SVG de Vender Call
        st.markdown("""
        - **Estrategia:** Apuestas a que el precio no subirá mucho
        - **Ganancia máxima:** Prima recibida ($5)
        - **Pérdida máxima:** Ilimitada
        - **Punto de equilibrio:** Strike + Prima
        """)

    with tabs_payoff[2]:
        st.markdown("### Comprar Put - Estrategia Bajista 📉")
        # Aquí insertaríamos el SVG de Comprar Put
        st.markdown("""
        - **Estrategia:** Apuestas a que el precio bajará
        - **Ganancia máxima:** Strike - Prima
        - **Pérdida máxima:** Prima pagada ($5)
        - **Punto de equilibrio:** Strike - Prima
        """)

    with tabs_payoff[3]:
        st.markdown("### Vender Put - Estrategia Alcista/Neutral 📈")
        # Aquí insertaríamos el SVG de Vender Put
        st.markdown("""
        - **Estrategia:** Apuestas a que el precio no bajará mucho
        - **Ganancia máxima:** Prima recibida ($5)
        - **Pérdida máxima:** Strike - Prima
        - **Punto de equilibrio:** Strike - Prima
        """)

    # Conclusión y tips
    st.markdown("""
    ### 💡 Tips para recordar:
    1. Las áreas verdes en los gráficos muestran dónde ganas dinero
    2. Las áreas rojas muestran dónde pierdes
    3. La prima es lo máximo que puedes perder al comprar opciones
    4. Al vender opciones, tus ganancias están limitadas pero las pérdidas pueden ser grandes
    """)

    # Botón para más información
    if st.button("¿Quieres aprender más sobre opciones? 📚"):
        st.markdown("""
        Aquí tienes algunos recursos adicionales:
        - [Guía de la CNBV sobre Opciones](https://ejemplo.com)
        - [Calculadora de Opciones](https://ejemplo.com)
        - [Simulador de Estrategias](https://ejemplo.com)
        """)



# Ver NOTICIAS -----------------------------------------------------------------------------------------------------------------------------

def get_news_for_ticker(ticker_symbol):
    """
    Obtiene noticias relacionadas con un ticker específico
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        
        if news:
            news_df = pd.DataFrame(news)
            news_df['providerPublishTime'] = pd.to_datetime(news_df['providerPublishTime'], unit='s')
            return split_df(news_df, 3)
        else:
            return None
    except Exception as e:
        st.error(f"Error al obtener noticias para {ticker_symbol}: {e}")
        return None


def split_df(df, n_splits):
    """
    Split a DataFrame into n_splits separate DataFrames of approximately equal size.
    
    Args:
        df (pd.DataFrame): Input DataFrame to split
        n_splits (int): Number of splits desired
        
    Returns:
        list: List of n_splits DataFrames
    """
    # Validate inputs
    if not isinstance(n_splits, int) or n_splits <= 0:
        raise ValueError("n_splits must be a positive integer")
    
    if n_splits > len(df):
        raise ValueError("n_splits cannot be larger than number of rows in DataFrame")
    
    # Calculate the approx size of each split
    split_size = len(df) // n_splits
    remainder = len(df) % n_splits
    
    result = []
    start = 0
    
    # Create the splits
    for i in range(n_splits):
        # Add one extra row to some splits if there's a remainder
        end = start + split_size + (1 if i < remainder else 0)
        result.append(df.iloc[start:end].copy())
        start = end
        
    return result
    


#CALCULADORA DE RIESGO ------------------------------------------------------------------------------------------------------

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calcula el precio de una opción usando Black-Scholes
    
    Parámetros:
    S: Precio actual del activo
    K: Precio de ejercicio
    T: Tiempo hasta vencimiento (en años)
    r: Tasa libre de riesgo
    sigma: Volatilidad
    option_type: 'call' o 'put'
    """
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type == 'call':
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    
    return price

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """
    Calcula los principales griegos de la opción
    """
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    # Delta
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    
    # Gamma (igual para calls y puts)
    gamma = norm.pdf(d1)/(S*sigma*np.sqrt(T))
    
    # Theta
    if option_type == 'call':
        theta = (-S*norm.pdf(d1)*sigma/(2*np.sqrt(T)) - 
                r*K*np.exp(-r*T)*norm.cdf(d2))
    else:
        theta = (-S*norm.pdf(d1)*sigma/(2*np.sqrt(T)) + 
                r*K*np.exp(-r*T)*norm.cdf(-d2))
    
    # Vega (igual para calls y puts)
    vega = S*np.sqrt(T)*norm.pdf(d1)
    
    return {
        'delta': delta,
        'gamma': gamma,
        'theta': theta/365,  # Convertido a días
        'vega': vega/100    # Convertido a puntos porcentuales
    }

def risk_calculator_tab():
    st.header("Calculadora de Riesgo para Opciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parámetros de la Opción")
        S = st.number_input("Precio actual del activo ($)", min_value=0.0, value=100.0)
        K = st.number_input("Precio de ejercicio ($)", min_value=0.0, value=100.0)
        T = st.slider("Tiempo hasta vencimiento (días)", min_value=1, max_value=365, value=30) / 365
        r = st.slider("Tasa libre de riesgo (%)", min_value=0.0, max_value=10.0, value=2.5) / 100
        sigma = st.slider("Volatilidad (%)", min_value=1.0, max_value=100.0, value=20.0) / 100
        option_type = st.selectbox("Tipo de opción", ['call', 'put'])

    # Calcular precio y griegos
    price = black_scholes(S, K, T, r, sigma, option_type)
    greeks = calculate_greeks(S, K, T, r, sigma, option_type)
    
    with col2:
        st.subheader("Resultados")
        st.metric("Precio de la Opción", f"${price:.2f}")
        
        # Mostrar los griegos
        col_delta, col_gamma = st.columns(2)
        col_theta, col_vega = st.columns(2)
        
        with col_delta:
            st.metric("Delta", f"{greeks['delta']:.3f}")
        with col_gamma:
            st.metric("Gamma", f"{greeks['gamma']:.3f}")
        with col_theta:
            st.metric("Theta", f"{greeks['theta']:.3f}")
        with col_vega:
            st.metric("Vega", f"{greeks['vega']:.3f}")
    
    # Análisis de sensibilidad
    st.subheader("Análisis de Sensibilidad")
    sensitivity_type = st.selectbox(
        "Seleccione el tipo de análisis",
        ['Precio del subyacente', 'Volatilidad', 'Tiempo hasta vencimiento']
    )
    
    if sensitivity_type == 'Precio del subyacente':
        prices = np.linspace(S*0.7, S*1.3, 100)
        values = [black_scholes(p, K, T, r, sigma, option_type) for p in prices]
        x_label = "Precio del subyacente"
        x_values = prices
    elif sensitivity_type == 'Volatilidad':
        vols = np.linspace(sigma*0.5, sigma*1.5, 100)
        values = [black_scholes(S, K, T, r, v, option_type) for v in vols]
        x_label = "Volatilidad"
        x_values = vols * 100  # Convertir a porcentaje
    else:
        times = np.linspace(T*0.1, T*2, 100)
        values = [black_scholes(S, K, t, r, sigma, option_type) for t in times]
        x_label = "Días hasta vencimiento"
        x_values = times * 365  # Convertir a días
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=values, mode='lines', name='Precio de la opción'))
    fig.update_layout(
        title=f"Sensibilidad al {sensitivity_type}",
        xaxis_title=x_label,
        yaxis_title="Precio de la opción ($)",
        hovermode='x'
    )
    st.plotly_chart(fig)
    
    # Añadir explicaciones
    with st.expander("ℹ️ Explicación de los Griegos"):
        st.markdown("""
        - **Delta**: Cambio en el precio de la opción por cada $1 de cambio en el subyacente
        - **Gamma**: Tasa de cambio del delta
        - **Theta**: Pérdida de valor por día debido al paso del tiempo
        - **Vega**: Cambio en el precio por cada 1% de cambio en la volatilidad
        """)















import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
import plotly.express as px

def create_interactive_visualizations():
    st.header("Visualizaciones Interactivas de Opciones")
    
    # Ya no necesitamos el selector ya que solo tendremos una opción
    create_payoff_diagram()

    

def create_strategy_explanation(strategy):
    """
    Proporciona explicaciones detalladas para cada estrategia de opciones
    """
    explanations = {
        "Call Largo": {
            "descripcion": """
            Un Call Largo es la compra de una opción call. Es una estrategia alcista que te da el derecho (pero no la obligación) 
            de comprar el activo subyacente a un precio determinado (strike price).
            """,
            "cuando_usar": """
            **¿Cuándo usar esta estrategia?**
            - Cuando esperas que el precio del activo suba significativamente
            - Cuando quieres apalancamiento con riesgo limitado
            - Cuando buscas exposición alcista con menos capital que comprando el activo directamente
            """,
            "caracteristicas": """
            **Características principales:**
            - Beneficio máximo: Ilimitado
            - Pérdida máxima: Prima pagada
            - Punto de equilibrio: Strike + Prima pagada
            - Delta: Positivo (0 a 1)
            """,
            "riesgos": """
            **Riesgos y consideraciones:**
            - Pérdida de la prima si el precio no sube lo suficiente
            - Afectado por el paso del tiempo (decay temporal)
            - Mayor impacto de la volatilidad
            """
        },
        "Put Largo": {
            "descripcion": """
            Un Put Largo es la compra de una opción put. Es una estrategia bajista que te da el derecho de vender 
            el activo subyacente a un precio determinado.
            """,
            "cuando_usar": """
            **¿Cuándo usar esta estrategia?**
            - Cuando esperas que el precio del activo baje
            - Como seguro para proteger posiciones largas
            - Para especular sobre movimientos bajistas con riesgo limitado
            """,
            "caracteristicas": """
            **Características principales:**
            - Beneficio máximo: Strike - Prima (cuando el precio llega a cero)
            - Pérdida máxima: Prima pagada
            - Punto de equilibrio: Strike - Prima pagada
            - Delta: Negativo (-1 a 0)
            """,
            "riesgos": """
            **Riesgos y consideraciones:**
            - Pérdida de la prima si el precio no baja
            - Afectado por el paso del tiempo
            - Generalmente más caras en mercados bajistas
            """
        },
        "Call Spread": {
            "descripcion": """
            Un Call Spread (o Bull Call Spread) implica comprar una call y vender otra con strike más alto. 
            Es una estrategia alcista con beneficio y riesgo limitados.
            """,
            "cuando_usar": """
            **¿Cuándo usar esta estrategia?**
            - Cuando esperas un movimiento alcista moderado
            - Cuando quieres reducir el costo de un call largo
            - Cuando prefieres limitar tanto pérdidas como ganancias
            """,
            "caracteristicas": """
            **Características principales:**
            - Beneficio máximo: Diferencia entre strikes - Prima neta pagada
            - Pérdida máxima: Prima neta pagada
            - Punto de equilibrio: Strike bajo + Prima neta
            - Delta: Positivo pero menor que un call largo
            """,
            "riesgos": """
            **Riesgos y consideraciones:**
            - Beneficio limitado por el strike superior
            - Requiere más capital que un call simple
            - Puede tener problemas de liquidez
            """
        },
        "Put Spread": {
            "descripcion": """
            Un Put Spread (o Bear Put Spread) implica comprar un put y vender otro con strike más bajo. 
            Es una estrategia bajista con beneficio y riesgo limitados.
            """,
            "cuando_usar": """
            **¿Cuándo usar esta estrategia?**
            - Cuando esperas un movimiento bajista moderado
            - Para reducir el costo de un put largo
            - Cuando buscas una estrategia bajista con riesgo definido
            """,
            "caracteristicas": """
            **Características principales:**
            - Beneficio máximo: Diferencia entre strikes - Prima neta pagada
            - Pérdida máxima: Prima neta pagada
            - Punto de equilibrio: Strike alto - Prima neta
            - Delta: Negativo pero menor que un put largo
            """,
            "riesgos": """
            **Riesgos y consideraciones:**
            - Beneficio limitado por el strike inferior
            - Requiere más capital que un put simple
            - El movimiento debe ser suficiente para superar las primas
            """
        },
        "Straddle": {
            "descripcion": """
            Un Straddle implica comprar simultáneamente un call y un put con el mismo strike y vencimiento. 
            Es una estrategia que busca beneficiarse de movimientos grandes en cualquier dirección.
            """,
            "cuando_usar": """
            **¿Cuándo usar esta estrategia?**
            - Cuando esperas un movimiento significativo pero no sabes la dirección
            - Antes de eventos importantes (earnings, FDA approvals, etc.)
            - Cuando la volatilidad implícita es baja pero esperas que aumente
            """,
            "caracteristicas": """
            **Características principales:**
            - Beneficio máximo: Ilimitado en ambas direcciones
            - Pérdida máxima: Suma de ambas primas
            - Dos puntos de equilibrio: Strike ± Suma de primas
            - Delta: Cerca de cero en el strike
            """,
            "riesgos": """
            **Riesgos y consideraciones:**
            - Costo elevado (dos primas)
            - Necesita un movimiento grande para ser rentable
            - Mayor exposición al decay temporal
            - Sensible a cambios en la volatilidad
            """
        },
        "Strangle": {
            "descripcion": """
            Un Strangle implica comprar un call y un put con diferentes strikes (put más bajo que call). 
            Similar al straddle pero con diferentes strikes y generalmente más barato.
            """,
            "cuando_usar": """
            **¿Cuándo usar esta estrategia?**
            - Cuando esperas un movimiento extremo pero no sabes la dirección
            - Cuando buscas una alternativa más barata al straddle
            - Cuando la volatilidad implícita es baja pero esperas que aumente
            """,
            "caracteristicas": """
            **Características principales:**
            - Beneficio máximo: Ilimitado en ambas direcciones
            - Pérdida máxima: Suma de ambas primas
            - Dos puntos de equilibrio más separados que el straddle
            - Delta: Varía según el precio del subyacente
            """,
            "riesgos": """
            **Riesgos y consideraciones:**
            - Necesita un movimiento más grande que el straddle para ser rentable
            - Menor costo pero mayor riesgo de pérdida total
            - Exposición al decay temporal
            - Mejor cuando se espera alta volatilidad
            """
        }
    }
    
    return explanations.get(strategy, {})

def create_payoff_diagram():
    st.subheader("Diagrama de Payoff para Estrategias de Opciones")
    
    # Parámetros de la estrategia
    col1, col2 = st.columns(2)
    
    with col1:
        strategy = st.selectbox(
            "Seleccione la estrategia:",
            ["Call Largo", "Put Largo", "Call Spread", "Put Spread", "Straddle", "Strangle"]
        )
        
        stock_price = st.number_input("Precio actual del subyacente:", value=100.0)
        strike = st.number_input("Strike Price:", value=100.0)
        
    with col2:
        premium = st.number_input("Prima de la opción:", value=5.0)
        if strategy in ["Call Spread", "Put Spread", "Strangle"]:
            strike2 = st.number_input("Strike Price 2:", value=110.0)
            premium2 = st.number_input("Prima 2:", value=2.0)
    
    # Crear rango de precios para el eje X
    price_range = np.linspace(stock_price * 0.5, stock_price * 1.5, 100)
    
    # Calcular payoff según la estrategia seleccionada
    if strategy == "Call Largo":
        payoff = np.maximum(price_range - strike, 0) - premium
    elif strategy == "Put Largo":
        payoff = np.maximum(strike - price_range, 0) - premium
    elif strategy == "Call Spread":
        payoff = (np.maximum(price_range - strike, 0) - premium) - (np.maximum(price_range - strike2, 0) - premium2)
    elif strategy == "Put Spread":
        payoff = (np.maximum(strike - price_range, 0) - premium) - (np.maximum(strike2 - price_range, 0) - premium2)
    elif strategy == "Straddle":
        payoff = np.maximum(price_range - strike, 0) + np.maximum(strike - price_range, 0) - (2 * premium)
    else:  # Strangle
        payoff = np.maximum(price_range - strike2, 0) + np.maximum(strike - price_range, 0) - (premium + premium2)
    
    # Crear gráfico con Plotly
    fig = go.Figure()
    
    # Añadir línea de payoff
    fig.add_trace(go.Scatter(
        x=price_range,
        y=payoff,
        mode='lines',
        name='Payoff',
        line=dict(color='blue')
    ))
    
    # Añadir línea de breakeven
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    
    # Personalizar el diseño
    fig.update_layout(
        title=f"Diagrama de Payoff - {strategy}",
        xaxis_title="Precio del Subyacente",
        yaxis_title="Profit/Loss",
        hovermode='x',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar explicación de la estrategia
    st.markdown("---")
    st.subheader("📚 Explicación de la Estrategia")
    
    explanation = create_strategy_explanation(strategy)
    if explanation:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Descripción")
            st.markdown(explanation["descripcion"])
            st.markdown("### ¿Cuándo Usar?")
            st.markdown(explanation["cuando_usar"])
            
        with col2:
            st.markdown("### Características")
            st.markdown(explanation["caracteristicas"])
            st.markdown("### Riesgos y Consideraciones")
            st.markdown(explanation["riesgos"])
        
        # Añadir visualización de riesgo/recompensa
        st.markdown("---")
        st.subheader("📊 Perfil de Riesgo/Recompensa")
        
        # Crear un gauge chart para visualizar el riesgo
        risk_reward = {
            "Call Largo": {"riesgo": 0.4, "potencial": 0.9},
            "Put Largo": {"riesgo": 0.4, "potencial": 0.9},
            "Call Spread": {"riesgo": 0.3, "potencial": 0.5},
            "Put Spread": {"riesgo": 0.3, "potencial": 0.5},
            "Straddle": {"riesgo": 0.7, "potencial": 0.8},
            "Strangle": {"riesgo": 0.6, "potencial": 0.8}
        }
        
        r_r = risk_reward.get(strategy, {"riesgo": 0.5, "potencial": 0.5})
        
        col1, col2 = st.columns(2)
        with col1:
            fig_risk = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = r_r["riesgo"] * 100,
                title = {'text': "Nivel de Riesgo"},
                gauge = {'axis': {'range': [0, 100]},
                        'bar': {'color': "red"},
                        'steps': [
                            {'range': [0, 33], 'color': "lightgreen"},
                            {'range': [33, 66], 'color': "yellow"},
                            {'range': [66, 100], 'color': "salmon"}]}))
            # Primer gauge (Riesgo)
        fig_risk = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = r_r["riesgo"] * 100,
            title = {'text': "Nivel de Riesgo"},
            gauge = {'axis': {'range': [0, 100]},
                    'bar': {'color': "red"},
                    'steps': [
                        {'range': [0, 33], 'color': "lightgreen"},
                        {'range': [33, 66], 'color': "yellow"},
                        {'range': [66, 100], 'color': "salmon"}]}))
        
        fig_risk.update_layout(height=400, width=600)  # Aumenté las dimensiones
        st.plotly_chart(fig_risk)
        
        # Segundo gauge (Potencial)
        fig_pot = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = r_r["potencial"] * 100,
            title = {'text': "Potencial de Ganancia"},
            gauge = {'axis': {'range': [0, 100]},
                    'bar': {'color': "green"},
                    'steps': [
                        {'range': [0, 33], 'color': "lightblue"},
                        {'range': [33, 66], 'color': "lightgreen"},
                        {'range': [66, 100], 'color': "green"}]}))
        
        fig_pot.update_layout(height=400, width=600)  # Aumenté las dimensiones
        st.plotly_chart(fig_pot)







        
#FACTORES QUE AFECTAN PRECIO DE OPCIONES--------------------------------------------------------------------------------------------------------

def display_option_price_factors():
    #st.header("Los 8 Factores que Afectan el Precio de las Opciones")
    
    # Crear tabs para cada factor
    factor_tabs = st.tabs([
        "1️⃣ Precio del Subyacente",
        "2️⃣ Strike Price",
        "3️⃣ Tiempo al Vencimiento",
        "4️⃣ Volatilidad",
        "5️⃣ Tasas de Interés",
        "6️⃣ Dividendos",
        "7️⃣ Oferta y Demanda",
        "8️⃣ Tipo de Opción"
    ])
    
    # Tab 1: Precio del Subyacente
    with factor_tabs[0]:
        st.subheader("Precio del Activo Subyacente")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            El precio del activo subyacente es uno de los factores más importantes que afecta el precio de una opción.
            
            **Para Opciones Call:**
            - ↑ Precio del subyacente = ↑ Precio de la call
            - ↓ Precio del subyacente = ↓ Precio de la call
            
            **Para Opciones Put:**
            - ↑ Precio del subyacente = ↓ Precio de la put
            - ↓ Precio del subyacente = ↑ Precio de la put
            """)
        
        with col2:
        
            st.info("💡 **Ejemplo:** Si tienes un call de AAPL con strike de 150 USD, su valor aumentará si el precio de AAPL sube de 145 a 155 USD.")
            
    # Tab 2: Strike Price
    with factor_tabs[1]:
        st.subheader("Precio de Ejercicio (Strike Price)")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            El strike price determina el precio al que se puede ejercer la opción.
            
            **Para Opciones Call:**
            - ↑ Strike Price = ↓ Precio de la opción
            - ↓ Strike Price = ↑ Precio de la opción
            
            **Para Opciones Put:**
            - ↑ Strike Price = ↑ Precio de la opción
            - ↓ Strike Price = ↓ Precio de la opción
            """)
        
        with col2:
            st.info("💡 **Ejemplo:** Un call con strike de 140 USD vale más que una call con strike de 160 USD (asumiendo que todos los demás factores son iguales.")

    # Tab 3: Tiempo al Vencimiento
    with factor_tabs[2]:
        st.subheader("Tiempo hasta el Vencimiento")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            El tiempo hasta el vencimiento afecta el valor temporal de la opción.
            
            **Efecto del Tiempo:**
            - Mayor tiempo = Más valor temporal
            - Menor tiempo = Menos valor temporal
            
            **Decaimiento Temporal:**
            - El decaimiento no es lineal
            - Se acelera cerca del vencimiento
            - Afecta más a las opciones At-The-Money
            """)
        
        with col2:
            st.info("💡 **Ejemplo:** Una opción que vence en 3 meses típicamente vale más que una opción idéntica que vence en 1 mes.")
    
    # Tab 4: Volatilidad
    with factor_tabs[3]:
        st.subheader("Volatilidad")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            La volatilidad mide la magnitud de los movimientos de precio del subyacente.
            
            **Tipos de Volatilidad:**
            1. **Volatilidad Histórica:** Basada en movimientos pasados
            2. **Volatilidad Implícita:** Derivada de los precios de mercado
            
            **Efecto en el Precio:**
            - ↑ Volatilidad = ↑ Precio de la opción
            - ↓ Volatilidad = ↓ Precio de la opción
            """)
        
        with col2:
            st.info("💡 **Ejemplo:** Las opciones suelen ser más caras antes de eventos importantes como reportes de ganancias debido a la mayor volatilidad esperada.")
    
    # Tab 5: Tasas de Interés
    with factor_tabs[4]:
        st.subheader("Tasas de Interés")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            Las tasas de interés libres de riesgo afectan el valor presente de los flujos futuros.
            
            **Efecto en las Opciones:**
            - ↑ Tasas = ↑ Precio de calls
            - ↑ Tasas = ↓ Precio de puts
            
            El efecto es generalmente menor comparado con otros factores.
            """)
        
        with col2:
            st.info("💡 **Ejemplo:** Un aumento en las tasas de interés de 2% a 3% tendría un efecto relativamente pequeño en el precio de las opciones.")
    
    # Tab 6: Dividendos
    with factor_tabs[5]:
        st.subheader("Dividendos")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            Los dividendos afectan el precio del subyacente y por ende el valor de las opciones.
            
            **Efecto de los Dividendos:**
            - ↑ Dividendos = ↓ Precio de calls
            - ↑ Dividendos = ↑ Precio de puts
            
            **Consideraciones:**
            - Fecha ex-dividendo
            - Monto del dividendo
            - Ajustes en el strike price
            """)
        
        with col2:
            st.info("💡 **Ejemplo:** Las opciones sobre acciones que pagan altos dividendos suelen tener diferentes precios que las opciones sobre acciones que no pagan dividendos.")
    
    # Tab 7: Oferta y Demanda
    with factor_tabs[6]:
        st.subheader("Oferta y Demanda")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            Las fuerzas del mercado pueden afectar significativamente los precios de las opciones.
            
            **Factores que Influyen:**
            - Volumen de negociación
            - Liquidez del mercado
            - Interés abierto
            - Eventos especiales
            - Sentimiento del mercado
            """)
        
        with col2:
            st.info("💡 **Ejemplo:** Durante eventos de alta volatilidad, la demanda por puts protectivas puede aumentar significativamente sus precios.")
    
    # Tab 8: Tipo de Opción
    with factor_tabs[7]:
        st.subheader("Tipo de Opción")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            El tipo de opción y sus características específicas afectan su precio.
            
            **Características Importantes:**
            - Americana vs. Europea
            - Call vs. Put
            - Estándar vs. Exótica
            - OTC vs. Listada
            
            **Consideraciones Adicionales:**
            - Restricciones de ejercicio
            - Ajustes contractuales
            - Regulaciones específicas
            """)
        
        with col2:
            st.info("💡 **Ejemplo:** Una opción americana (que puede ejercerse en cualquier momento) generalmente vale más que una opción europea equivalente (que solo puede ejercerse al vencimiento).")
    
# Resumen visual
    st.subheader("Resumen de Impacto en el Precio")
    
    # Crear tabla de impacto con los 8 factores
    impact_data = {
        'Factor': [
            'Precio Subyacente ↑', 
            'Strike Price ↑', 
            'Tiempo al Vencimiento ↑', 
            'Volatilidad ↑', 
            'Tasas de Interés ↑', 
            'Dividendos ↑',
            'Oferta > Demanda',
            'Tipo de Opción (Americana vs. Europea)'
        ],
        'Call Options': ['↑', '↓', '↑', '↑', '↑', '↓', '↑', '↑'],
        'Put Options': ['↓', '↑', '↑', '↑', '↓', '↑', '↑', '↑']
    }
    
    df = pd.DataFrame(impact_data)
    
    # Aplicar estilos a la tabla
    styled_df = df.style\
        .set_properties(**{'text-align': 'center'})\
        .set_properties(subset=['Factor'], **{'text-align': 'left'})\
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center')]},
            {'selector': 'td', 'props': [('padding', '8px')]},
            {'selector': '', 'props': [('border', '1px solid #ddd')]},
            {'selector': 'tbody tr:nth-of-type(odd)', 'props': [('background-color', 'rgba(255, 255, 255, 0.05)')]}
        ])
    
    st.table(styled_df)
    
    st.markdown("""
    ---
    **Nota:** Es importante recordar que estos factores no actúan de manera aislada, 
    sino que interactúan entre sí de formas complejas. La comprensión de cómo cada 
    factor afecta el precio de las opciones es fundamental para el trading exitoso.
    
    **Leyenda:**
    - ↑ : Incremento en el precio
    - ↓ : Disminución en el precio
    - Para el factor "Tipo de Opción", se asume que las opciones americanas generalmente tienen un valor mayor o igual que las europeas debido a su flexibilidad de ejercicio.
    """)














#ANÁLISIS DE SENISIBLIIDAD-------------------------------------------------------------------------------------------------------------------------
def create_sensitivity_analysis():
    st.subheader("Análisis de Sensibilidad")
    
    # Parámetros
    col1, col2 = st.columns(2)
    
    with col1:
        factor = st.selectbox(
            "Factor a analizar:",
            ["Volatilidad", "Tiempo", "Tasa de Interés"]
        )
        option_type = st.selectbox("Tipo de Opción:", ["Call", "Put"])
        
    with col2:
        stock_price = st.number_input("Precio del subyacente:", value=100.0)
        strike = st.number_input("Strike:", value=100.0)
    
    # Crear gráfico 3D
    if factor == "Volatilidad":
        x = np.linspace(0.1, 0.5, 20)  # Volatilidad
        y = np.linspace(stock_price * 0.7, stock_price * 1.3, 20)  # Precio
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        for i in range(len(x)):
            for j in range(len(y)):
                Z[j,i] = black_scholes(Y[j,i], strike, 0.25, 0.02, X[i], option_type.lower())
        
        fig = go.Figure(data=[go.Surface(x=X*100, y=Y, z=Z)])
        fig.update_layout(
            title='Superficie de Sensibilidad',
            scene = dict(
                xaxis_title='Volatilidad (%)',
                yaxis_title='Precio del Subyacente',
                zaxis_title='Precio de la Opción'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

def create_volatility_surface():
    st.subheader("Superficie de Volatilidad Implícita")
    
    # Generar datos de ejemplo para la superficie de volatilidad
    strikes = np.linspace(80, 120, 20)
    times = np.linspace(0.1, 1, 20)
    X, Y = np.meshgrid(strikes, times)
    
    # Crear una superficie de volatilidad sintética
    Z = 0.2 + 0.1 * np.exp(-((X - 100)**2)/1000) + 0.05 * np.exp(-((Y - 0.5)**2)/0.1)
    
    fig = go.Figure(data=[go.Surface(x=X, y=Y*252, z=Z*100)])
    fig.update_layout(
        title='Superficie de Volatilidad Implícita',
        scene = dict(
            xaxis_title='Strike Price',
            yaxis_title='Días al Vencimiento',
            zaxis_title='Volatilidad Implícita (%)'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calcula el precio de una opción usando el modelo Black-Scholes
    
    Parámetros:
    S: Precio actual del activo
    K: Precio de ejercicio
    T: Tiempo hasta vencimiento (en años)
    r: Tasa libre de riesgo
    sigma: Volatilidad
    option_type: 'call' o 'put'
    """
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type == 'call':
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    
    return price





#EXPLICACIÓN MATRIZ RIESGO-------------------------------------------------------------------------------------------------------








def show_risk_explanation():
   explanation = """
   # 📚 ¿Qué son los Scores de Impacto y Probabilidad?

   ¡Hola! 👋 Vamos a entender juntos qué son los Scores de Impacto y Probabilidad de una manera sencilla.

   Imagina que estás planeando una inversión - estos scores son como tu "detector de riesgos" personal. Son súper útiles para tomar decisiones más informadas.

   ## 🎯 SCORE DE IMPACTO:
   Este score nos dice "¿qué tanto nos podría afectar si algo sale mal?". Es como medir la intensidad del golpe si las cosas no van como esperamos.

   * Se califica normalmente del 1 al 5 (o del 1 al 10)
   * ¿Qué mide exactamente? Piensa en:
       * ¿Cuánto dinero podrías perder?
       * ¿Cómo afectaría a la empresa en el mercado?
       * ¿Se podría dañar la reputación de la empresa?
       * ¿Podría afectar su funcionamiento diario?
       * ¿Habría problemas con reguladores o autoridades?

   ## 🎲 SCORE DE PROBABILIDAD:
   Este es más como adivinar el clima - ¿qué tan probable es que llueva? Pero en este caso, ¿qué tan probable es que algo salga mal?

   * También se califica con números (como el impacto)
   * Toma en cuenta cosas como:
       * ¿Ha pasado antes? (historia)
       * ¿Cómo está el mercado ahora?
       * ¿Qué está pasando en esa industria?
       * ¿Hay factores externos que puedan afectar?
       * ¿Qué tan bien se maneja la empresa internamente?

   ## 💡 ¿Por qué son importantes?
   Imagina que estás pensando en invertir en opciones de una empresa tecnológica. Estos scores te ayudan a:
   * Entender mejor los riesgos antes de invertir
   * Comparar diferentes inversiones
   * Tomar decisiones más inteligentes con tu dinero
   * Dormir más tranquilo sabiendo que has evaluado los riesgos

   ## 🔑 Tip práctico:
   Multiplica el Score de Impacto por el de Probabilidad para obtener tu "Score de Riesgo Total".
   Por ejemplo, si el impacto es 3 y la probabilidad es 2, tu riesgo total sería 6.
   """
   return explanation

# Para usar en Streamlit:
# with st.expander("📚 ¿Qué son los Scores de Impacto y Probabilidad? (Click para expandir)"):
#     st.markdown(show_risk_explanation())