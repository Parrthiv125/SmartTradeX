from smarttradex_core.prediction.predictor import Predictor


def run_test():

    predictor = Predictor()

    prediction = predictor.predict(
        {"return": 0.001},
        {"return": 0.002}
    )

    print(prediction)


if __name__ == "__main__":
    run_test()
