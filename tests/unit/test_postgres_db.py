from datetime import datetime
from smarttradex_core.database.postgres_db import PostgresDB


db = PostgresDB()

# -------------------------------
# Test connection
# -------------------------------
print("DB Time:", db.test_connection())

# -------------------------------
# Insert trade
# -------------------------------
db.insert_trade(
    entry_time=datetime.now(),
    side="LONG",
    entry_price=53000,
    quantity=0.01,
    confidence=0.82,
    strategy="Momentum"
)

print("Trade inserted.")

# -------------------------------
# Fetch last open trade
# -------------------------------
trade_id = db.get_last_open_trade()
print("Last open trade:", trade_id)

# -------------------------------
# Close trade
# -------------------------------
db.close_trade(
    trade_id=trade_id,
    exit_time=datetime.now(),
    exit_price=53500,
    pnl_pct=0.94,
    pnl_value=5
)

print("Trade closed.")
