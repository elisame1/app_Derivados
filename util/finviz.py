import streamlit as st
import requests
import pandas as pd

# Crear el diccionario con las industrias
INDUSTRIES = [
    "All",
    "Basic Materials",
    "Communication Services",
    "Consumer Cyclical",
    "Consumer Defensive",
    "Energy",
    "Financial",
    "Healthcare",
    "Industrials",
    "Real Estate",
    "Technology",
    "Utilities",
    "Custom"
]


def generar_url(vista, filtros):
    return st.secrets["FINVIZ_ENDPOINT"] + "?v=" + str(vista) + "&f=" + filtros + "&auth=" + st.secrets["FINVIZ_API_KEY"]


def descargar_datos(vista, filtros, ruta):
    response = requests.get(generar_url(vista, filtros))
    if response.status_code == 200:
        with open(ruta, "wb") as f:
            f.write(response.content)
    else:
        raise Exception("Error en la descarga de datos de Finviz")

#guardar archivos en una carpeta para descargarlos y unir los tres archivos
@st.cache_data
def get_finviz_dataframe(filtros):
    overview_path = "data/finviz_technical111.csv"
    performance_path = "data/finviz_performance141.csv"
    financial_path = "data/finviz_financial161.csv"
    technical_path = "data/finviz_technical171.csv"
    ownership_path = "data/finviz_ownership131.csv"

    descargar_datos(111, filtros, overview_path)
    descargar_datos(141, filtros, performance_path)
    descargar_datos(161, filtros, financial_path)
    descargar_datos(171, filtros, technical_path)
    descargar_datos(131, filtros, ownership_path)

    # los archivos descargados los convertimos en DFrame cada uno
    overview_df = pd.read_csv(overview_path, index_col=1)
    performance_df = pd.read_csv(performance_path, index_col=1)
    financial_df = pd.read_csv(financial_path, index_col=1)
    technical_df = pd.read_csv(technical_path, index_col=1)
    ownership_df = pd.read_csv(ownership_path, index_col=1)

    # convertir porcentajes a decimal
    performance_df['Volatility (Month)'] = performance_df['Volatility (Month)'].str.rstrip('%').astype('float') / 100.0
    ownership_df['Short Float'] = ownership_df['Short Float'].str.rstrip('%').astype('float') / 100.0
    
    output_df = pd.DataFrame({
        'Company': overview_df['Company'],
        'Sector': overview_df['Sector'],
        'Market Cap': overview_df['Market Cap'],
        'Volume': overview_df['Volume'],
    }, index=overview_df.index) #nuevo data frame que combina los cuatro anteriores
    
    #merge columns we want to use
    output_df = output_df.join(performance_df[['Performance (Year)', 'Volatility (Month)', 'Average Volume']])
    output_df = output_df.join(financial_df[['Total Debt/Equity', 'Return on Assets', 'Return on Equity', 'Return on Investment']])
    output_df = output_df.join(technical_df[['Beta', 'Relative Strength Index (14)']])
    output_df = output_df.join(ownership_df[['Short Float']])
    output_df = output_df.dropna()

    return output_df

get_finviz_dataframe('')
