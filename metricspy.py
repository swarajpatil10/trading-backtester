import numpy as np
import pandas as pd

def calculate_metrics(data: pd.DataFrame, initial_capital: float = 100000.0) -> dict:
    final_value = data["portfolio_value"].iloc[-1]
    total_return_pct = ((final_value - initial_capital) / initial_capital) * 100

    # Daily returns of the portfolio (not the stock)
    daily_returns = data["portfolio_value"].pct_change().dropna()

    # Max drawdown: largest peak-to-trough decline
    running_max = data["portfolio_value"].cummax()
    drawdown = (data["portfolio_value"] - running_max) / running_max
    max_drawdown_pct = drawdown.min() * 100

    # Sharpe ratio: mean daily return / std of daily return, annualized (assume 0% risk-free rate)
    if daily_returns.std() != 0:
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0

    # Win rate: % of completed trades (buy->sell pairs) that were profitable
    trades = data[data["position"] != 0].copy()
    trade_returns = []
    buy_price = None

    for _, row in trades.iterrows():
        if row["position"] == 1:
            buy_price = row["Close"]
        elif row["position"] == -1 and buy_price is not None:
            trade_returns.append((row["Close"] - buy_price) / buy_price)
            buy_price = None

    if trade_returns:
        win_rate_pct = (sum(1 for r in trade_returns if r > 0) / len(trade_returns)) * 100
    else:
        win_rate_pct = 0.0

    return {
        "total_return_pct": round(total_return_pct, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "win_rate_pct": round(win_rate_pct, 2),
        "final_portfolio_value": round(final_value, 2),
    }