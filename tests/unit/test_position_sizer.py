from smarttradex_core.trading.position_sizer import PositionSizer

def run_test():
    capital = 10000  # $10,000 paper capital
    price = 50000    # BTC price

    sizer = PositionSizer(capital, 0.02)
    qty = sizer.calculate_position_size(price)

    print("Calculated quantity:", qty)

    assert qty > 0
    print("PositionSizer test passed")

if __name__ == "__main__":
    run_test()
