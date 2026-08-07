# routers/backtest.py
from fastapi import APIRouter, Depends, HTTPException
import yfinance as yf

from models import BacktestRequest, BacktestResult
from database import get_connection
from dependencies import get_current_user
from strategy import add_moving_averages, generate_signals, simulate_trades
from metrics import calculate_metrics

router = APIRouter(prefix="/backtest", tags=["backtest"])


@router.post("/run", response_model=BacktestResult)
def run_backtest(request: BacktestRequest, current_user: dict = Depends(get_current_user)):
    data = yf.download(request.ticker, start=request.start_date, end=request.end_date)

    if data.empty:
        raise HTTPException(status_code=400, detail="No data found for this ticker/date range")

    data.columns = data.columns.get_level_values(0)

    data = add_moving_averages(data, request.short_window, request.long_window)
    data = generate_signals(data)
    data = simulate_trades(data, request.initial_capital)

    results = calculate_metrics(data, request.initial_capital)

    # Save to database
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO backtests (user_id, ticker, strategy_name, start_date, end_date, params)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            current_user["id"],
            request.ticker,
            "MA Crossover",
            request.start_date,
            request.end_date,
            '{"short_window": %d, "long_window": %d, "initial_capital": %f}' % (
                request.short_window, request.long_window, request.initial_capital
            ),
        )
    )
    backtest_id = cur.fetchone()[0]

    cur.execute(
        """
        INSERT INTO backtest_results (backtest_id, total_return, max_drawdown, sharpe_ratio, win_rate, final_portfolio_value)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            backtest_id,
            float(results["total_return_pct"]),
            float(results["max_drawdown_pct"]),
            float(results["sharpe_ratio"]),
            float(results["win_rate_pct"]),
            float(results["final_portfolio_value"]),
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    return {
        "ticker": request.ticker,
        "start_date": request.start_date,
        "end_date": request.end_date,
        **results
    }


@router.get("/history")
def get_backtest_history(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT b.id, b.ticker, b.strategy_name, b.start_date, b.end_date, b.created_at,
               r.total_return, r.max_drawdown, r.sharpe_ratio, r.win_rate, r.final_portfolio_value
        FROM backtests b
        JOIN backtest_results r ON b.id = r.backtest_id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
        """,
        (current_user["id"],)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "ticker": row[1],
            "strategy_name": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "created_at": row[5],
            "total_return_pct": row[6],
            "max_drawdown_pct": row[7],
            "sharpe_ratio": row[8],
            "win_rate_pct": row[9],
            "final_portfolio_value": row[10],
        }
        for row in rows
    ]


@router.get("/{backtest_id}")
def get_backtest_detail(backtest_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT b.id, b.ticker, b.strategy_name, b.start_date, b.end_date, b.params, b.created_at,
               r.total_return, r.max_drawdown, r.sharpe_ratio, r.win_rate, r.final_portfolio_value
        FROM backtests b
        JOIN backtest_results r ON b.id = r.backtest_id
        WHERE b.id = %s AND b.user_id = %s
        """,
        (backtest_id, current_user["id"])
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return {
        "id": row[0],
        "ticker": row[1],
        "strategy_name": row[2],
        "start_date": row[3],
        "end_date": row[4],
        "params": row[5],
        "created_at": row[6],
        "total_return_pct": row[7],
        "max_drawdown_pct": row[8],
        "sharpe_ratio": row[9],
        "win_rate_pct": row[10],
        "final_portfolio_value": row[11],
    }