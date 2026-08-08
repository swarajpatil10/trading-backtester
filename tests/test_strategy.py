import pandas as pd
from strategy import add_moving_averages, generate_signals, simulate_trades

def make_sample_data():
    prices = [100, 102, 101, 105, 108, 110, 107, 106, 109, 112]
    return pd.DataFrame({"Close": prices})


def test_add_moving_averages_creates_columns():
    data = make_sample_data()
    result = add_moving_averages(data, short_window=2, long_window=4)
    assert "short_ma" in result.columns
    assert "long_ma" in result.columns


def test_generate_signals_creates_position_column():
    data = make_sample_data()
    data = add_moving_averages(data, short_window=2, long_window=4)
    result = generate_signals(data)
    assert "signal" in result.columns
    assert "position" in result.columns


def test_simulate_trades_tracks_portfolio_value():
    data = make_sample_data()
    data = add_moving_averages(data, short_window=2, long_window=4)
    data = generate_signals(data)
    result = simulate_trades(data, initial_capital=1000.0)
    assert "portfolio_value" in result.columns
    assert result["portfolio_value"].iloc[0] > 0