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
    """
    Core trading engine.
    One call to step() = one market update + one decision.
    """

    def __init__(self):
        # ── Engine state (API visible) ─────────────────
        self.state = EngineState()
        self.running = False

        # ── Market data ───────────────────────────────
        self.exchange = BinanceClient()
        self.market_feed = MarketFeed(self.exchange)
        self.candle_buffer = CandleBuffer(max_size=100)

        # ── AI pipeline ───────────────────────────────
        self.feature_engine = FeatureEngine()
        self.predictor = Predictor()
        self.marker_factory = MarkerFactory()

        # ── Paper trading ─────────────────────────────
        self.paper_broker = PaperBroker()

    # ────────────────────────────────────────────────
    # Lifecycle
    # ────────────────────────────────────────────────

    def start(self):
        if self.running:
            return
        self.running = True
        print("[ENGINE] Started")

    def stop(self):
        if not self.running:
            return
        self.running = False
        print("[ENGINE] Stopped")

    def reset(self):
        self.state.reset()
        self.candle_buffer.clear()
        print("[ENGINE] Reset")

    # ────────────────────────────────────────────────
    # Core execution
    # ────────────────────────────────────────────────

    def step(self):
        """
        Execute exactly ONE engine cycle.
        Safe to be called repeatedly from runtime loop.
        """

        # Engine must be running
        if not self.running:
            return None

        # 1️⃣ Fetch market data
        candle = self.market_feed.update()
        if candle is None:
            return None

        close_price = candle.get("close")
        if close_price is None:
            return None

        # 2️⃣ Store candle
        self.candle_buffer.add_candle(candle)

        # Update state early (GUI sees live price)
        self.state.market_data = candle

        candles = self.candle_buffer.get_all()

        # 3️⃣ Wait until enough data exists
        if len(candles) < 5:
            return {
                "price": close_price,
                "status": "warming_up"
            }

        # 4️⃣ Build features
        features = self.feature_engine.build_features(candles)
        if features is None:
            return None

        # 5️⃣ Prediction
        prediction = self.predictor.predict(features)
        self.state.prediction = prediction

        # 6️⃣ Marker decision
        marker = self.marker_factory.create_marker(prediction)
        self.state.markers.append(marker)

        # 7️⃣ Paper trading
        trade = self.paper_broker.process_marker(marker, close_price)
        if trade:
            self.state.trades.append(trade)

        return {
            "price": close_price,
            "prediction": prediction,
            "marker": marker,
            "trade": trade,
        }
