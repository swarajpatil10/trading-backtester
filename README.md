# Trading Backtester API

A backend API for backtesting algorithmic trading strategies against real historical stock market data. Users can register, authenticate, and run a Moving Average Crossover strategy on any stock ticker, then view performance metrics like return, drawdown, and Sharpe ratio — with every backtest saved to their account for later review.

**Live API:** https://trading-backtester-api-xdyy.onrender.com/docs
**Repository:** https://github.com/swarajpatil10/trading-backtester

> Note: hosted on Render's free tier, so the first request after inactivity may take 30–50 seconds while the server spins up.

---

## What it does

1. A user registers and logs in, receiving a JWT access token
2. They submit a stock ticker (e.g. `RELIANCE.NS`, `AAPL`), a date range, and optional strategy parameters
3. The backend pulls real historical price data, runs a Moving Average Crossover strategy, and simulates trades against a starting capital of ₹100,000 (configurable)
4. It calculates total return, maximum drawdown, Sharpe ratio, win rate, and final portfolio value
5. Every backtest is saved to the database and can be retrieved later, scoped to that user only

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Framework | FastAPI | Automatic request validation via Pydantic, async-capable, auto-generated OpenAPI/Swagger docs |
| Database | PostgreSQL (raw `psycopg2`, no ORM) | Deliberately avoided an ORM to build a solid understanding of SQL and connection handling |
| Auth | JWT (`python-jose`) + `passlib`/bcrypt | Stateless token-based auth, standard for APIs without server-rendered pages |
| Market data | `yfinance` | Free historical OHLCV data, including Indian tickers (`.NS` suffix) |
| Data processing | `pandas`, `numpy` | Rolling averages, signal generation, trade simulation, metrics |
| Testing | `pytest` | Unit tests for strategy and metrics logic |
| Deployment | Render | Web service + managed PostgreSQL |

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/auth/register` | Create a new user | No |
| POST | `/auth/login` | Log in, returns a JWT access token | No |
| GET | `/auth/me` | Get the currently logged-in user | Yes |

### Backtest
| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/backtest/run` | Run a backtest and save the result | Yes |
| GET | `/backtest/history` | List all of the user's past backtests | Yes |
| GET | `/backtest/{id}` | Get full detail of one backtest | Yes |

Full interactive documentation (with request/response schemas) is available at `/docs` on both the local and live deployment.

---

## Strategy: Moving Average Crossover

The implemented strategy computes a short-window and long-window rolling average of closing price. When the short MA crosses above the long MA, it's treated as a buy signal; when it crosses below, a sell signal. All capital is deployed on a buy signal and liquidated on a sell signal — a simple, well-known strategy chosen for its clarity and testability, as a foundation the project is designed to build on (see Roadmap below).

**Metrics calculated:**
- **Total return %** — overall portfolio growth over the period
- **Max drawdown %** — the largest peak-to-trough decline, a measure of downside risk
- **Sharpe ratio** — return per unit of risk, annualized
- **Win rate %** — percentage of completed (buy→sell) trades that were profitable
- **Final portfolio value**

---

## Architecture decisions

- **API-first, no server-rendered frontend** — pure JSON API, testable directly through Swagger UI, with a thin client to be added later
- **JWT over sessions** — the server issues a signed token on login; the client sends it via `Authorization: Bearer <token>` on subsequent requests, avoiding server-side session state
- **Strategy logic kept separate from the API layer** (`strategy.py`, `metrics.py`) — these are pure functions with no FastAPI or database dependency, tested independently via pytest before ever being wired into an endpoint
- **Input validation at the model layer** — Pydantic validators reject invalid date ranges, non-positive capital, and non-positive MA windows before the request reaches any business logic
- **User-scoped data access** — every backtest query filters by the authenticated user's ID, so users can never view or access another user's backtests, even by guessing an ID

---

## Real bugs hit and fixed during development

- **Null-byte corrupted file:** an empty `__init__.py` created via PowerShell's `>` redirect was written in UTF-16, inserting null bytes that Python's import system rejected with a cryptic `SyntaxError`. Fixed by recreating the file through the editor instead of a shell redirect.
- **passlib/bcrypt version incompatibility:** `passlib 1.7.4`'s internal self-test breaks against `bcrypt >= 4.0`, producing a misleading `"password cannot be longer than 72 bytes"` error regardless of actual password length. Fixed by pinning `bcrypt==4.0.1`.
- **Misplaced route functions:** during a manual edit, two endpoint functions were accidentally pasted in the middle of another function's body, silently breaking route registration without raising an error until the routes simply didn't appear in Swagger. Fixed by carefully restructuring the file and verifying route counts in `/docs` after every change.

---

## Running locally

```bash
# Clone and enter the project
git clone https://github.com/swarajpatil10/trading-backtester.git
cd trading-backtester

# Set up virtual environment
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create a .env file)
# DATABASE_URL=postgresql://user:password@localhost:5432/trading_backtester
# JWT_SECRET_KEY=your-secret-key-here

# Create database tables
python create_tables.py

# Run the server
uvicorn main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Running tests

```bash
python -m pytest tests/
```

---

## Roadmap

- [ ] Frontend (HTML/JS + Chart.js) for a visual backtest history and equity curve
- [ ] Additional strategies (RSI, Bollinger Bands, MACD)
- [ ] ML-based strategy (Version 2) using `scikit-learn`, benchmarked against the rule-based strategy on Sharpe ratio and drawdown using the same backtesting engine
- [ ] Support for backtesting a portfolio of multiple tickers simultaneously

---

## Author

Built by [Swaraj Patil](https://github.com/swarajpatil10) — B.Tech Electronics & Telecommunication Engineering student, self-teaching backend development.