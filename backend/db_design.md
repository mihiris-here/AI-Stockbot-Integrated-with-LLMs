Sure! Here's your **stock portfolio database schema** written in clean, markdown format for documentation purposes:

---

## 📊 Stock Portfolio Database Schema (Solo Trader)

### Overview  
This schema is designed for a **self-managed trading system**. It logs all stock transactions, tracks real-time holdings, maintains price history, and includes a simplified balance sheet to monitor cash and assets.

---

### 🧱 Tables

---

#### **1. `Stocks`**  
Stores information about all stocks traded.

| Column       | Type        | Description                    |
|--------------|-------------|--------------------------------|
| stock_id     | SERIAL      | Primary key                    |
| symbol       | VARCHAR(10) | Ticker symbol (e.g., AAPL)     |
| name         | VARCHAR(100)| Full name of the stock         |
| exchange     | VARCHAR(20) | Exchange name (e.g., NASDAQ)   |
| category     | VARCHAR(20) | The Industry the company is in |

---

#### **2. `Transactions`**  
Logs each transaction made by the trader.

| Column           | Type         | Description                                                    |
|------------------|--------------|----------------------------------------------------------------|
| transaction_id   | SERIAL       | Primary key                                                    |
| stock_id         | INT          | Foreign key to `Stocks`                                        |
| transaction_type | VARCHAR(10)  | 'BUY', 'SELL', 'DIVIDEND', 'DEPOSIT', or 'WITHDRAWAL'         |
| quantity         | DECIMAL      | Number of shares (or 0 for cash-only transactions)            |
| price_per_share  | DECIMAL      | Price per share (if applicable)                                |
| total_value      | DECIMAL      | Total value of the transaction                                 |
| transaction_date | TIMESTAMP    | Timestamp of the transaction                                   |
| notes            | TEXT         | Optional description or notes                                  |

---

#### **3. `Holdings`**  
Tracks current positions in each stock.

| Column        | Type     | Description                                  |
|---------------|----------|----------------------------------------------|
| holding_id    | SERIAL   | Primary key                                  |
| stock_id      | INT      | Foreign key to `Stocks`                      |
| quantity      | DECIMAL  | Number of shares currently held              |
| avg_price     | DECIMAL  | Average purchase price                       |
| last_updated  | TIMESTAMP| Last time the holding was modified           |

---

#### **4. `Prices`**  
Stores historical stock prices to calculate portfolio market value.

| Column     | Type     | Description                          |
|------------|----------|--------------------------------------|
| price_id   | SERIAL   | Primary key                          |
| stock_id   | INT      | Foreign key to `Stocks`              |
| price      | DECIMAL  | Closing price                        |
| date       | TIMESTAMP| Date the price was recorded          |

---

#### **5. `BalanceSheet`**  
Tracks available cash and estimated total asset value.

| Column        | Type     | Description                                                        |
|---------------|----------|--------------------------------------------------------------------|
| balance_id    | SERIAL   | Primary key                                                        |
| cash          | DECIMAL  | Current available cash                                             |
| total_assets  | DECIMAL  | Cash + value of current holdings (based on latest stock prices)   |
| last_updated  | TIMESTAMP| Last time balance sheet was refreshed                              |


---

#### **6. `InvestigationQueue`**  
Tracks stocks that are under consideration for future trades, monitoring, or research.

| Column         | Type        | Description                                                    |
|----------------|-------------|----------------------------------------------------------------|
| queue_id       | SERIAL      | Primary key                                                    |
| reason         | TEXT        | Notes or reasoning for the investigation                       |
| priority       | VARCHAR(10) | Optional flag: 'LOW', 'MEDIUM', 'HIGH'                         |
| added_date     | TIMESTAMP   | Date the stock was added to the queue                          |
| last_reviewed  | TIMESTAMP   | Most recent date the stock was evaluated                       |
| action_taken   | VARCHAR(20) | 'NONE', 'WATCHING', 'BUY', 'SKIPPED', 'REMOVED'                |

---

#### **7. `Stocks_Under_Investigation`**  
| Column         | Type        | Description                                                    |
|----------------|-------------|----------------------------------------------------------------|
| queue_id       | SERIAL      | Primary key                                                    |
| stock_id       | INT         | Foreign key to `Stocks`                                        |
| reason         | TEXT        | Notes or reasoning for the investigation on that stock specifically|

