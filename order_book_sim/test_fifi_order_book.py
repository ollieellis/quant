from order_book_sim import FifoOrderBook
from models import Order, OrderType

class TestInit:

    def test_constructor(self):
        orders = [
            Order(0, 100, 1, True, OrderType.market),
            Order(0, 101, 1, True, OrderType.market),
            Order(0, 102, 1, True, OrderType.market),
        ]
        FifoOrderBook(orders)

class TestMarketOrder:

    def test_simple_market_order(self):
        orders = [
            Order(0, 102, 1, True, OrderType.market),
            Order(0, 101, 1, True, OrderType.market),
            Order(0, 100, 1, True, OrderType.market),
        ]
        order_book = FifoOrderBook(orders)
        trades = order_book.market_buy(1)
        # assert len(orders) == 1

class TestLimitOrderBuy:

    def test_limits_in_constructor(self):
        orders = [Order(0, 100, 1, True, OrderType.market)]
        order_book = FifoOrderBook(orders)
        trades = order_book.market_buy(1)
