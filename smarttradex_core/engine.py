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
        # ── Engine state (API / GUI visible) ───────────
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

        if not self.running:
            return None

        # 1️⃣ Fetch latest market candle
        candle = self.market_feed.update()
        if candle is None:
            return None

        close_price = candle.get("close")
        if close_price is None:
            return None

        # 2️⃣ Store candle in buffer
        self.candle_buffer.add_candle(candle)

        # Update live market state early (GUI needs this)
        self.state.market_data = candle

        candles = self.candle_buffer.get_all()

        # 3️⃣ Warm-up phase (need at least 5 candles)
        if len(candles) < 5:
            return {
                "price": close_price,
                "status": "warming_up"
            }

        # 4️⃣ Build 1-minute features
        features_1m = self.feature_engine.build_features(candles)
        if features_1m is None:
            return None

        # 5️⃣ Build 5-minute candle + features
        candle_5m = self.candle_buffer.get_last_5m_candle()
        features_5m = self.feature_engine.build_5m_features(candle_5m)

        # Store all features in engine state (clean & explicit)
        self.state.features = {
            "1m": features_1m,
            "5m": features_5m
        }

        # 6️⃣ Prediction (still uses 1m for now)
        prediction = self.predictor.predict(features_1m)
        self.state.prediction = prediction

        # 7️⃣ Marker generation
        marker = self.marker_factory.create_marker(prediction)

        # Deduplicate markers (store only if action changes)
        if not self.state.markers or self.state.markers[-1]["action"] != marker["action"]:
            self.state.markers.append(marker)

        # 8️⃣ Paper trading
        trade = self.paper_broker.process_marker(marker, close_price)
        if trade:
            self.state.trades.append(trade)

        return {
            "price": close_price,
            "prediction": prediction,
            "marker": marker,
            "trade": trade,
        }
