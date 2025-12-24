import sqlite3
import datetime

from strategies.demo_strat import DemoStrategy
from base_forecasting import BaseForecasting  # your MC subclass
from alpaca_api import (
    get_historical_bars,
    get_current_price,
    place_market_order
)
import LinearRegression

DB_PATH = "bot.db"
SYMBOL = "AAPL"
TRADE_QTY = 1


def get_db() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def get_stock_id(conn, symbol):
    cur = conn.cursor()
    cur.execute("SELECT stock_id FROM Stocks WHERE symbol = ?", (symbol,))
    return cur.fetchone()[0]


def get_holding(conn, stock_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT quantity, avg_price FROM Holdings WHERE stock_id = ?",
        (stock_id,)
    )
    row = cur.fetchone()
    if row:
        return row[0], row[1]
    return 0.0, 0.0


def update_holdings_buy(conn, stock_id, qty, price):
    cur = conn.cursor()

    q_old, p_old = get_holding(conn, stock_id)

    q_new = q_old + qty
    p_new = price if q_old == 0 else (q_old * p_old + qty * price) / q_new

    if q_old == 0:
        cur.execute(
            "INSERT INTO Holdings (stock_id, quantity, avg_price) VALUES (?, ?, ?)",
            (stock_id, q_new, p_new)
        )
    else:
        cur.execute(
            "UPDATE Holdings SET quantity = ?, avg_price = ?, last_updated = CURRENT_TIMESTAMP WHERE stock_id = ?",
            (q_new, p_new, stock_id)
        )


def update_holdings_sell(conn, stock_id, qty, price):
    cur = conn.cursor()

    q_old, p_old = get_holding(conn, stock_id)
    assert qty <= q_old

    q_new = q_old - qty

    if q_new == 0:
        cur.execute("DELETE FROM Holdings WHERE stock_id = ?", (stock_id,))
    else:
        cur.execute(
            "UPDATE Holdings SET quantity = ?, last_updated = CURRENT_TIMESTAMP WHERE stock_id = ?",
            (q_new, stock_id)
        )


def insert_transaction(conn, stock_id, action, qty, price):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Transactions
        (stock_id, transaction_type, quantity, price_per_share, total_value, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            stock_id,
            action,
            qty,
            price,
            qty * price,
            datetime.datetime.now(datetime.timezone.utc)
        )
    )

def insert_decision_log(
    conn, stock_id, expected_price, current_price,
    action, confidence, model_name, strategy_name
):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO DecisionLog
        (stock_id, expected_price, current_price, action, confidence, model_name, strategy_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (stock_id, expected_price, current_price, action, confidence, model_name, strategy_name)
    )



def main():
    conn = get_db()
    stock_id = get_stock_id(conn, SYMBOL)

    # ---- DATA ----
    data = get_historical_bars(SYMBOL, lookback_days=60)
    current_price = get_current_price(SYMBOL)

    # ---- FORECAST ----
    model = LinearRegression.LinearRegressionForecasting(SYMBOL, data)
    model.run()
    forecast = model.get_forecast()

    # ---- DECISION LOG (ALWAYS LOG, EVEN HOLD) ----
    insert_decision_log(
        conn=conn,
        stock_id=stock_id,
        expected_price=forecast["expected_price"],
        current_price=current_price,
        action=decision,
        confidence=forecast.get("confidence"),
        model_name=model.__class__.__name__,
        strategy_name=strat.__class__.__name__
    )

    # ---- STRATEGY ----
    qty_held, _ = get_holding(conn, stock_id)
    strat = DemoStrategy()
    decision = strat.decide(forecast, current_price, qty_held)

    if decision == "BUY":
        fill_price = place_market_order(SYMBOL, "buy", TRADE_QTY)
        update_holdings_buy(conn, stock_id, TRADE_QTY, fill_price)
        insert_transaction(conn, stock_id, "BUY", TRADE_QTY, fill_price)

    elif decision == "SELL":
        fill_price = place_market_order(SYMBOL, "sell", TRADE_QTY)
        update_holdings_sell(conn, stock_id, TRADE_QTY, fill_price)
        insert_transaction(conn, stock_id, "SELL", TRADE_QTY, fill_price)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
