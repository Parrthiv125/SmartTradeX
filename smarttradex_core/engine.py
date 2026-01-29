# smarttradex_core/engine.py

from smarttradex_core.state import EngineState
from smarttradex_core.data.binance_client import BinanceClient
from smarttradex_core.data.market_feed import MarketFeed
from smarttradex_core.data.candle_buffer import CandleBuffer
from smarttradex_core.features.feature_engine import FeatureEngine
from smarttradex_core.prediction.predictor import Predictor


class TradingEngine:
    def __init__(self):
        self.state = EngineState()
        self.running = False

        # market data components
        self.exchange = BinanceClient()
        self.market_feed = MarketFeed(self.exchange)
        self.candle_buffer = CandleBuffer(max_size=100)

        # AI components
        self.feature_engine = FeatureEngine()
        self.predictor = Predictor()

    def start(self):
        if self.running:
            return
        self.running = True
        print("Engine started")

    def stop(self):
        if not self.running:
            return
        self.running = False
        print("Engine stopped")

    def reset(self):
        self.state.reset()
        self.candle_buffer.clear()
        print("Engine state reset")

    def step(self):
        """
        Single engine step:
        fetch data → features → prediction
        """
        candle = self.market_feed.update()
        self.candle_buffer.add_candle(candle)

        features = self.feature_engine.build_features(
            self.candle_buffer.get_all()
        )

        prediction = self.predictor.predict(features)

        self.state.market_data = candle
        self.state.prediction = prediction

        return prediction
