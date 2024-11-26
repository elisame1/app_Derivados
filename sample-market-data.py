import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Create sample data for 20 companies
tickers = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META',
    'TSLA', 'NVDA', 'JPM', 'BAC', 'WMT',
    'PG', 'JNJ', 'V', 'MA', 'DIS',
    'NFLX', 'INTC', 'AMD', 'CRM', 'PYPL'
]

# Generate realistic-looking data
data = {
    'Market Cap': np.random.uniform(50e9, 2e12, 20),  # 50B to 2T
    'Volatility (Month)': np.random.uniform(0.15, 0.45, 20),  # 15% to 45%
    'Total Debt/Equity': np.random.uniform(0.3, 2.5, 20),  # 0.3 to 2.5
    'Relative Strength Index (14)': np.random.uniform(30, 70, 20),  # 30 to 70
    'Volume': np.random.uniform(1e6, 50e6, 20),  # 1M to 50M
    'Average Volume': np.random.uniform(1e6, 50e6, 20),  # 1M to 50M
    'Short Float': np.random.uniform(0.01, 0.15, 20)  # 1% to 15%
}

# Create DataFrame
df = pd.DataFrame(data, index=tickers)

# Adjust values to be more realistic for specific companies
# Large tech companies (higher market cap, lower debt)
tech_companies = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
df.loc[tech_companies, 'Market Cap'] *= 1.5
df.loc[tech_companies, 'Total Debt/Equity'] *= 0.7

# Financial companies (higher debt/equity)
financial_companies = ['JPM', 'BAC']
df.loc[financial_companies, 'Total Debt/Equity'] *= 1.8

# Growth companies (higher volatility and RSI)
growth_companies = ['TSLA', 'NVDA', 'AMD']
df.loc[growth_companies, 'Volatility (Month)'] *= 1.4
df.loc[growth_companies, 'Short Float'] *= 1.3

# Round values for better readability
df['Market Cap'] = df['Market Cap'].round(2)
df['Volatility (Month)'] = df['Volatility (Month)'].round(4)
df['Total Debt/Equity'] = df['Total Debt/Equity'].round(2)
df['Relative Strength Index (14)'] = df['Relative Strength Index (14)'].round(2)
df['Volume'] = df['Volume'].round(0)
df['Average Volume'] = df['Average Volume'].round(0)
df['Short Float'] = df['Short Float'].round(4)

# Save to CSV
df.to_csv('sample_market_data.csv')

# Display first few rows to verify
print(df.head())
