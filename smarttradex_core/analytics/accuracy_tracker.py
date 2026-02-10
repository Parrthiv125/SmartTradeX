from collections import deque


class AccuracyTracker:
    """
    Tracks prediction accuracy in live trading
    """

    def __init__(self, window_size=100):

        self.window_size = window_size

        # Stores True/False prediction correctness
        self.history = deque(maxlen=window_size)

        self.total_predictions = 0
        self.correct_predictions = 0

    # --------------------------------------------------
    # RECORD PREDICTION RESULT
    # --------------------------------------------------
    def record_prediction(
        self,
        predicted_return,
        actual_return
    ):
        """
        Compare predicted vs actual direction
        """

        predicted_direction = 1 if predicted_return > 0 else -1
        actual_direction = 1 if actual_return > 0 else -1

        is_correct = predicted_direction == actual_direction

        self.history.append(is_correct)

        self.total_predictions += 1
        if is_correct:
            self.correct_predictions += 1

        return is_correct

    # --------------------------------------------------
    # ROLLING ACCURACY
    # --------------------------------------------------
    def rolling_accuracy(self):

        if not self.history:
            return 0.0

        return (
            sum(self.history) / len(self.history)
        ) * 100

    # --------------------------------------------------
    # GLOBAL ACCURACY
    # --------------------------------------------------
    def overall_accuracy(self):

        if self.total_predictions == 0:
            return 0.0

        return (
            self.correct_predictions /
            self.total_predictions
        ) * 100

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------
    def summary(self):

        return {
            "rolling_accuracy": round(
                self.rolling_accuracy(), 2
            ),
            "overall_accuracy": round(
                self.overall_accuracy(), 2
            ),
            "total_predictions": self.total_predictions
        }
