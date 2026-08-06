from database import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS backtests (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            ticker VARCHAR(20) NOT NULL,
            strategy_name VARCHAR(50) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            params JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS backtest_results (
            id SERIAL PRIMARY KEY,
            backtest_id INTEGER REFERENCES backtests(id),
            total_return FLOAT,
            max_drawdown FLOAT,
            sharpe_ratio FLOAT,
            win_rate FLOAT,
            final_portfolio_value FLOAT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()