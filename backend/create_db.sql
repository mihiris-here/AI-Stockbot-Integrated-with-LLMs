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
CREATE TABLE Prices (
    price_id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES Stocks(stock_id),
    price DECIMAL(15, 4) NOT NULL,
    date TIMESTAMP NOT NULL
);
CREATE TABLE BalanceSheet (
    balance_id SERIAL PRIMARY KEY,
    cash DECIMAL(20, 4) NOT NULL DEFAULT 0.0,
    total_assets DECIMAL(20, 4) GENERATED ALWAYS AS (
        cash + (
            SELECT COALESCE(SUM(h.quantity * p.price), 0)
            FROM Holdings h
            JOIN Prices p ON p.stock_id = h.stock_id
            WHERE p.date = (SELECT MAX(date) FROM Prices WHERE stock_id = h.stock_id)
        )
    ) STORED,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE InvestigationQueue (
    queue_id SERIAL PRIMARY KEY,
    reason TEXT,
    priority VARCHAR(10) CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reviewed TIMESTAMP,
    action_taken VARCHAR(20) CHECK (action_taken IN ('NONE', 'WATCHING', 'BUY', 'SKIPPED', 'REMOVED'))
);
CREATE TABLE Stocks_Under_Investigation (
    queue_id INT REFERENCES InvestigationQueue(queue_id) ON DELETE CASCADE,
    stock_id INT REFERENCES Stocks(stock_id),
    reason TEXT,
    PRIMARY KEY (queue_id, stock_id)
);

