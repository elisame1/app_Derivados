import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def calculate_impact_score(df):
    """Calculate impact score based on volatility, leverage and market cap"""
    # Normalize values between 0 and 1
    volatility_norm = (df['Volatility (Month)'] - df['Volatility (Month)'].min()) / (df['Volatility (Month)'].max() - df['Volatility (Month)'].min())
    leverage_norm = (df['Total Debt/Equity'] - df['Total Debt/Equity'].min()) / (df['Total Debt/Equity'].max() - df['Total Debt/Equity'].min())
    mcap_norm = (df['Market Cap'] - df['Market Cap'].min()) / (df['Market Cap'].max() - df['Market Cap'].min())
    
    # Weighted average (adjust weights as needed)
    impact_score = (0.4 * volatility_norm + 0.4 * leverage_norm + 0.2 * mcap_norm)
    return impact_score

def calculate_probability_score(df):
    """Calculate probability score based on RSI, liquidity ratio and short float"""
    # Normalize values between 0 and 1
    rsi_norm = (df['Relative Strength Index (14)'] - df['Relative Strength Index (14)'].min()) / (df['Relative Strength Index (14)'].max() - df['Relative Strength Index (14)'].min())
    liquidity_ratio = df['Average Volume'] / df['Volume']
    liquidity_norm = (liquidity_ratio - liquidity_ratio.min()) / (liquidity_ratio.max() - liquidity_ratio.min())
    short_float_norm = (df['Short Float'] - df['Short Float'].min()) / (df['Short Float'].max() - df['Short Float'].min())
    
    # Weighted average (adjust weights as needed)
    probability_score = (0.4 * rsi_norm + 0.3 * liquidity_norm + 0.3 * short_float_norm)
    return probability_score

def create_risk_matrix(df):
    """Create risk matrix visualization using plotly"""
    impact_scores = calculate_impact_score(df)
    probability_scores = calculate_probability_score(df)
    
    fig = go.Figure()
    
    # Add scatter plot
    fig.add_trace(go.Scatter(
        x=probability_scores,
        y=impact_scores,
        mode='markers+text',
        text=df.index,
        textposition="top center",
        marker=dict(
            size=10,
            color='blue',
            opacity=0.6
        ),
        hovertemplate="<br>".join([
            "Ticker: %{text}",
            "Impact Score: %{y:.2f}",
            "Probability Score: %{x:.2f}",
            "<extra></extra>"
        ])
    ))
    
    # Add quadrant lines
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray")
    fig.add_vline(x=0.5, line_dash="dash", line_color="gray")
    
    # Update layout
    fig.update_layout(
        title="Risk Matrix - Derivative Investment",
        xaxis_title="Probability of Adverse Event",
        yaxis_title="Potential Impact",
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1]),
        width=800,
        height=800,
        showlegend=False
    )
    
    # Add quadrant labels
    fig.add_annotation(x=0.25, y=0.75, text="High Impact/<br>Low Probability", showarrow=False)
    fig.add_annotation(x=0.75, y=0.75, text="High Impact/<br>High Probability", showarrow=False)
    fig.add_annotation(x=0.25, y=0.25, text="Low Impact/<br>Low Probability", showarrow=False)
    fig.add_annotation(x=0.75, y=0.25, text="Low Impact/<br>High Probability", showarrow=False)
    
    return fig

def main():
    st.title("Matriz de Riesgo para Inversión en Derivados")
    
    st.write("""
    Esta aplicación analiza datos de mercado para crear una matriz de riesgo 2x2 para inversión en derivados.
    
    ### Cómo interpretar la matriz:
    - **Eje Y (Impacto Potencial)**: Combina volatilidad mensual, ratio de apalancamiento y capitalización de mercado
    - **Eje X (Probabilidad de Evento Adverso)**: Combina RSI, ratio de liquidez y short float
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Cargar archivo CSV con datos de mercado", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, index_col=0)
            
            # Display risk matrix
            fig = create_risk_matrix(df)
            st.plotly_chart(fig)
            
            # Display risk categories
            st.subheader("Categorización de Riesgo por Ticker")
            
            risk_df = pd.DataFrame({
                'Impact Score': calculate_impact_score(df),
                'Probability Score': calculate_probability_score(df)
            })
            
            def categorize_risk(row):
                if row['Impact Score'] > 0.5 and row['Probability Score'] > 0.5:
                    return "Alto Riesgo"
                elif row['Impact Score'] > 0.5:
                    return "Riesgo de Impacto"
                elif row['Probability Score'] > 0.5:
                    return "Riesgo de Probabilidad"
                else:
                    return "Bajo Riesgo"
            
            risk_df['Risk Category'] = risk_df.apply(categorize_risk, axis=1)
            st.dataframe(risk_df)
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
            st.write("Por favor, asegúrese de que el archivo CSV contiene todas las columnas necesarias:")
            st.write("- Market Cap")
            st.write("- Volatility (Month)")
            st.write("- Total Debt/Equity")
            st.write("- Relative Strength Index (14)")
            st.write("- Volume")
            st.write("- Average Volume")
            st.write("- Short Float")

if __name__ == "__main__":
    main()
