import pandas as pd

performance_df = pd.read_csv('data/finviz_performance141.csv', index_col=1)
performance_df['Volatility (Week)'] = performance_df['Volatility (Week)'].str.rstrip('%').astype('float') / 100.0

