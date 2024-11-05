from order_book_sim import FifoOrderBook
from models import LimitOrder
from datetime import datetime

class TestInit:

    def test_bid_constructor(self):
        LimitOrders = [
            LimitOrder(ID=0, price=100, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=2, price=102, volume=1, buy=True, creation_time=datetime.now()),
        ]
        book = FifoOrderBook(LimitOrders)
        prices = []
        # while book.bid.qsize():
            # print("Im cooked")
        for i in range(3):
            prices.append(book.bid.get(timeout=1).price)
        assert prices == [102, 101, 100]

    def test_ask_constructor(self):
        LimitOrders = [
            LimitOrder(ID=1, price=101, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=2, price=102, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=0, price=100, volume=1, buy=False, creation_time=datetime.now()),
        ]
        book = FifoOrderBook(LimitOrders)
        prices = []
        # while book.bid.qsize():
            # print("Im cooked")
        for i in range(3):
            prices.append(book.ask.get(timeout=1).price)
        assert prices == [100, 101, 102]


class TestMarketLimitOrder:

    def test_simple_market_LimitOrder(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=True, creation_time=datetime.now()),
        ]
        LimitOrder_book =  FifoOrderBook(LimitOrders)
        # buy_LimitOrder = LimitOrder(ID=4)
        trades = LimitOrder_book.market_buy(1)
        # assert len(LimitOrders) == 1

class TestLimitLimitOrderBuy:

    def test_limits_in_constructor(self):
        LimitOrders = [
            LimitOrder(ID=0, price=100, volume=1, buy=True, creation_time=datetime.now())
        ]
        LimitOrder_book =  FifoOrderBook(LimitOrders)
        trades = LimitOrder_book.market_buy(1)
        print(LimitOrder_book.bid)