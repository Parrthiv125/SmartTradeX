from smarttradex_core.data.candle_buffer import CandleBuffer

buffer = CandleBuffer(max_size=2)

buffer.add_candle({"close": 100})
buffer.add_candle({"close": 101})

assert len(buffer.get_all()) == 2

buffer.add_candle({"close": 102})
assert len(buffer.get_all()) == 2
assert buffer.get_all()[0]["close"] == 101

buffer.clear()
assert buffer.get_all() == []

print("CandleBuffer test passed")
