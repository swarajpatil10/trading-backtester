import pandas as pd

def add_moving_averages(data: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
    data = data.copy()
    data["short_ma"] = data["Close"].rolling(window=short_window).mean()
    data["long_ma"] = data["Close"].rolling(window=long_window).mean()
    return data


def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["signal"] = 0

    # 1 = short MA above long MA (bullish), 0 = otherwise
    data.loc[data["short_ma"] > data["long_ma"], "signal"] = 1

    # position change: +1 = buy, -1 = sell, 0 = no change
    data["position"] = data["signal"].diff()

    return data

def simulate_trades(data: pd.DataFrame, initial_capital: float = 100000.0) -> pd.DataFrame:
    data = data.copy()
    data["holding"] = 0       # 1 = holding stock, 0 = holding cash
    data["portfolio_value"] = initial_capital

    cash = initial_capital
    shares = 0
    holding = 0

    portfolio_values = []

    for i in range(len(data)):
        price = data["Close"].iloc[i]
        position = data["position"].iloc[i]

        # Buy signal and not already holding
        if position == 1 and holding == 0:
            shares = cash / price
            cash = 0
            holding = 1

        # Sell signal and currently holding
        elif position == -1 and holding == 1:
            cash = shares * price
            shares = 0
            holding = 0

        current_value = cash + (shares * price)
        portfolio_values.append(current_value)
        data.iloc[i, data.columns.get_loc("holding")] = holding

    data["portfolio_value"] = portfolio_values
    return data