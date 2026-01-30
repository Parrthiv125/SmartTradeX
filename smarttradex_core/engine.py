# smarttradex_core/engine.py

from smarttradex_core.state import EngineState
from smarttradex_core.data.binance_client import BinanceClient
from smarttradex_core.data.market_feed import MarketFeed
from smarttradex_core.data.candle_buffer import CandleBuffer
from smarttradex_core.features.feature_engine import FeatureEngine
from smarttradex_core.prediction.predictor import Predictor
from smarttradex_core.markers.marker_factory import MarkerFactory
from smarttradex_core.trading.paper_broker import PaperBroker


class TradingEngine:
    def __init__(self):
        self.state = EngineState()
        self.running = False

        # market data
        self.exchange = BinanceClient()
        self.market_feed = MarketFeed(self.exchange)
        self.candle_buffer = CandleBuffer(max_size=100)

        # AI
        self.feature_engine = FeatureEngine()
        self.predictor = Predictor()
        self.marker_factory = MarkerFactory()

        # paper trading
        self.paper_broker = PaperBroker()

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
        Full engine step:
        data → prediction → marker → paper trade
        """
        candle = self.market_feed.update()
        price = candle.get("close", 0.0)

        self.candle_buffer.add_candle(candle)

        features = self.feature_engine.build_features(
            self.candle_buffer.get_all()
        )

        prediction = self.predictor.predict(features)
        marker = self.marker_factory.create_marker(prediction)

        trade = self.paper_broker.process_marker(marker, price)

        self.state.market_data = candle
        self.state.prediction = prediction
        self.state.markers.append(marker)

        if trade:
            self.state.trades.append(trade)

        return {
            "marker": marker,
            "trade": trade
        }
