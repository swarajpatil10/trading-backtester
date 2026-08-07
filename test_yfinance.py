import yfinance as yf
from strategy import add_moving_averages, generate_signals, simulate_trades
from metrics import calculate_metrics

ticker = "RELIANCE.NS"
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")
data.columns = data.columns.get_level_values(0)

data = add_moving_averages(data)
data = generate_signals(data)
data = simulate_trades(data)

results = calculate_metrics(data)
print(results)