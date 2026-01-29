from smarttradex_core.engine import TradingEngine

engine = TradingEngine()

engine.start()

for _ in range(3):
    engine.fetch_market_data()

assert engine.state.market_data is not None
assert len(engine.candle_buffer.get_all()) == 3

engine.reset()
assert len(engine.candle_buffer.get_all()) == 0

engine.stop()

print("TradingEngine candle buffer integration test passed")
