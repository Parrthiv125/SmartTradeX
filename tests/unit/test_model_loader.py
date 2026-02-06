from smarttradex_core.models.model_loader import ModelLoader


def run_test():

    loader = ModelLoader(
        "models_store/btc_5m_model"
    )

    model, scaler = loader.load()

    print("Model loaded:", model is not None)

    print("Scaler loaded:", scaler is not None)

    print("ModelLoader test passed")


if __name__ == "__main__":
    run_test()
