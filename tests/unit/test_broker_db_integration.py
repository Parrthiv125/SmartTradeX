from smarttradex_core.trading.paper_broker import PaperBroker


# Initialize broker
broker = PaperBroker()


# -------------------------------
# STEP 1 — ENTRY MARKER
# -------------------------------
buy_marker = {
    "action": "BUY",
    "confidence": 0.85
}

entry_price = 54000

broker.process_marker(
    marker=buy_marker,
    price=entry_price
)

print("Entry processed.")


# -------------------------------
# STEP 2 — EXIT MARKER
# -------------------------------
sell_marker = {
    "action": "SELL",
    "confidence": 0.80
}

exit_price = 54500

trade = broker.process_marker(
    marker=sell_marker,
    price=exit_price
)

print("Exit processed.")
print("Trade result:", trade)
