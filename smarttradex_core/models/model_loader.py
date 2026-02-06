import joblib
import os


class ModelLoader:
    """
    Loads trained ML models and scalers.
    """

    def __init__(self, model_path: str):

        self.model_path = model_path

        self.model = None
        self.scaler = None

    # ─────────────────────────────────────────────
    # LOAD MODEL
    # ─────────────────────────────────────────────
    def load(self):

        model_file = os.path.join(
            self.model_path,
            "model.pkl"
        )

        scaler_file = os.path.join(
            self.model_path,
            "scaler.pkl"
        )

        if not os.path.exists(model_file):
            raise FileNotFoundError(
                f"Model not found: {model_file}"
            )

        self.model = joblib.load(model_file)

        if os.path.exists(scaler_file):
            self.scaler = joblib.load(scaler_file)

        return self.model, self.scaler
