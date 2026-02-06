class BaseStrategy:
    """
    Parent class for all strategies.
    Ensures consistent signal output format.
    """

    def generate_signal(self, prediction: dict):
        """
        Must return marker dict:

        {
            "action": "BUY / SELL / HOLD",
            "confidence": float,
            "strategy": str
        }
        """
        raise NotImplementedError(
            "Strategy must implement generate_signal()"
        )
