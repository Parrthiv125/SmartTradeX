from smarttradex_core.trading.pnl_calculator import PnLCalculator

calc = PnLCalculator()

trade = {
    "side": "BUY",
    "entry_price": 100,
    "exit_price": 110
}

result = calc.calculate(trade)

assert result["pnl"] == 10
assert round(result["pnl_pct"], 2) == 10.0

print("PnLCalculator test passed")
