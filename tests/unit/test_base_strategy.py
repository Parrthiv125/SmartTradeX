from smarttradex_core.strategies.base_strategy import BaseStrategy


def run_test():

    try:
        s = BaseStrategy()
        s.generate_signal({})
    except NotImplementedError:
        print("BaseStrategy test passed")


if __name__ == "__main__":
    run_test()
