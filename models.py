from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    email:EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"    

class BacktestRequest(BaseModel):
    ticker: str
    start_date: date
    end_date: date
    short_window: int = 20
    long_window: int = 50
    initial_capital: float = 100000.0


class BacktestResult(BaseModel):
    ticker: str
    start_date: date
    end_date: date
    total_return_pct: float
    max_drawdown_pct: float
    sharpe_ratio: float
    win_rate_pct: float
    final_portfolio_value: float    
