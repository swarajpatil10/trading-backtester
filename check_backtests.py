from database import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT id, user_id, ticker, strategy_name, start_date, end_date, params FROM backtests;")
print("--- backtests ---")
for row in cur.fetchall():
    print(row)

cur.execute("SELECT id, backtest_id, total_return, max_drawdown, sharpe_ratio, win_rate, final_portfolio_value FROM backtest_results;")
print("\n--- backtest_results ---")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()