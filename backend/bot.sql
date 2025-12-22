CREATE TABLE Stocks (
    stock_id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    exchange VARCHAR(20), 
    category VARCHAR(20)
);
CREATE TABLE Transactions (
    transaction_id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES Stocks(stock_id),
    transaction_type VARCHAR(10) CHECK (transaction_type IN ('BUY', 'SELL', 'DIVIDEND', 'DEPOSIT', 'WITHDRAWAL')),
    quantity DECIMAL(15, 4),
    price_per_share DECIMAL(15, 4),
    total_value DECIMAL(20, 4),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
CREATE TABLE Holdings (
    holding_id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES Stocks(stock_id),
    quantity DECIMAL(15, 4) NOT NULL CHECK (quantity >= 0),
    avg_price DECIMAL(15, 4) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE BalanceSheet (
    balance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cash REAL NOT NULL DEFAULT 0.0,
    last_valued_assets REAL,      -- snapshot, not generated
    last_valuation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
