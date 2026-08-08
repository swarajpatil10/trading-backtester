from pydantic import BaseModel, EmailStr, field_validator
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

class BacktestRequest(BaseModel):
    ticker: str
    start_date: date
    end_date: date
    short_window: int = 20
    long_window: int = 50
    initial_capital: float = 100000.0

    @field_validator("end_date")
    @classmethod
    def end_date_after_start(cls, v, info):
        start = info.data.get("start_date")
        if start and v <= start:
            raise ValueError("end_date must be after start_date")
        return v

    @field_validator("initial_capital")
    @classmethod
    def capital_positive(cls, v):
        if v <= 0:
            raise ValueError("initial_capital must be greater than 0")
        return v

    @field_validator("short_window", "long_window")
    @classmethod
    def windows_positive(cls, v):
        if v <= 0:
            raise ValueError("window must be greater than 0")
        return v