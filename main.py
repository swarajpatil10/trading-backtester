from fastapi import FastAPI
from routers import auth
from routers import auth, backtest

app = FastAPI()

app.include_router(auth.router)
app.include_router(backtest.router)

@app.get("/")
def root():
    return {"message": "Trading Backtester API running"}