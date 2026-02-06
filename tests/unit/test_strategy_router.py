from smarttradex_core.strategies.strategy_router import StrategyRouter


def run_test():

    router = StrategyRouter()

    prediction = {
        "action": "BUY",
        "confidence": 0.8
    }

    regimes = ["trend", "range", "volatile", "unknown"]

    for r in regimes:
        signal = router.route(prediction, r)
        print(f"{r} → {signal}")

    print("Strategy router test passed")


if __name__ == "__main__":
    run_test()
