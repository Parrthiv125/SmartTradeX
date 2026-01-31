from smarttradex_core.data.candle_buffer import CandleBuffer

buffer = CandleBuffer(max_size=10)

# Add 5 fake 1-minute candles
for i in range(5):
    buffer.add_candle({
        "timestamp": i,
        "open": 100 + i,
        "high": 105 + i,
        "low": 95,
        "close": 102 + i,
        "volume": 10
    })

candle_5m = buffer.get_last_5m_candle()

assert candle_5m is not None
assert candle_5m["open"] == 100
assert candle_5m["close"] == 106
assert candle_5m["high"] == 109
assert candle_5m["low"] == 95
assert candle_5m["volume"] == 50

print("5-minute candle aggregation test PASSED")
