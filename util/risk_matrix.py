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

def create_matrix(df):
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
