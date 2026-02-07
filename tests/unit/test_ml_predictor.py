from smarttradex_core.prediction.predictor import Predictor


def run_test():

    predictor = Predictor()

    features = {
        "ret_1": 0.001,
        "ret_5": 0.002,
        "ret_15": 0.003,
        "vol_5": 40,
        "vol_15": 70
    }

    prediction = predictor.predict(features)

    print(prediction)


if __name__ == "__main__":
    run_test()
