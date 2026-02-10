from smarttradex_core.trading.paper_broker import PaperBroker
import time


broker = PaperBroker()

# Disable cooldown for testing
broker.trade_cooldown_seconds = 0


# --------------------------------------
# Trade 1 — WIN
# --------------------------------------
buy_marker = {
    "action": "BUY",
    "confidence": 0.85,
    "strategy": "Momentum"
}

broker.process_marker(
    marker=buy_marker,
    price=50000
)

time.sleep(1)

sell_marker = {
    "action": "SELL",
    "confidence": 0.80,
    "strategy": "Momentum"
}

broker.process_marker(
    marker=sell_marker,
    price=51000
)


# --------------------------------------
# Trade 2 — LOSS
# --------------------------------------
broker.process_marker(
    marker=buy_marker,
    price=52000
)

time.sleep(1)

broker.process_marker(
    marker=sell_marker,
    price=51000
)


# --------------------------------------
# Print Reinforcement Summary
# --------------------------------------
print("\nReinforcement Summary:")
print(broker.get_reinforcement_summary())
