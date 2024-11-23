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


class TestMarketBuyOrder:

    def test_simple_market_buy_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=False, creation_time=datetime.now()),
        ]
        limit_order_book =  FifoOrderBook(LimitOrders)
        trades = limit_order_book.market_buy(2)
        assert len(trades) == 2
        assert limit_order_book.ask.qsize() == 1
        ask_min =  limit_order_book.ask.get(timeout=0.1)
        assert ask_min.price == 102
        assert ask_min.volume == 1 

    def test_partial_market_buy_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=2, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=False, creation_time=datetime.now()),
        ]
        limit_order_book =  FifoOrderBook(LimitOrders)
        trades = limit_order_book.market_buy(2)
        assert len(trades) == 2
        assert limit_order_book.ask.qsize() == 2
        ask_min =  limit_order_book.ask.get(timeout=0.1)
        assert ask_min.price == 101
        assert ask_min.volume == 1

class TestMarketSellOrder:

    def test_simple_market_sell_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=True, creation_time=datetime.now()),
        ]
        limit_order_book = FifoOrderBook(LimitOrders)
        trades = limit_order_book.market_sell(2)
        assert len(trades) == 2
        assert limit_order_book.bid.qsize() == 1
        bid_max =  limit_order_book.bid.get(timeout=0.1)
        assert bid_max.price == 100
        assert bid_max.volume == 1

    def test_partial_market_sell_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=2, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=True, creation_time=datetime.now()),
        ]
        limit_order_book = FifoOrderBook(LimitOrders)
        trades = limit_order_book.market_sell(2)
        assert len(trades) == 2
        assert limit_order_book.bid.qsize() == 2
        bid_max =  limit_order_book.bid.get(timeout=0.1)
        assert bid_max.price == 101
        assert bid_max.volume == 1

class TestLimitBuyOrder:

    def test_simple_limit_buy_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=False, creation_time=datetime.now()),
        ]
        limit_order_book = FifoOrderBook(LimitOrders)
        new_order = LimitOrder(ID=3, price=103, volume=2, buy=True, creation_time=datetime.now())
        trades = limit_order_book.limit_order_buy(new_order)
        assert len(trades) == 2
        assert limit_order_book.ask.qsize() == 1
        ask_min = limit_order_book.ask.get(timeout=0.1)
        assert ask_min.price == 102
        assert ask_min.volume == 1

    def test_partial_limit_buy_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=2, buy=False, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=False, creation_time=datetime.now()),
        ]
        limit_order_book = FifoOrderBook(LimitOrders)
        new_order = LimitOrder(ID=3, price=101, volume=2, buy=True, creation_time=datetime.now())
        trades = limit_order_book.limit_order_buy(new_order)
        assert len(trades) == 2
        assert limit_order_book.ask.qsize() == 2
        ask_min = limit_order_book.ask.get(timeout=0.1)
        assert ask_min.price == 101
        assert ask_min.volume == 1


class TestLimitSellOrder:

    def test_simple_limit_sell_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=True, creation_time=datetime.now()),
        ]
        limit_order_book = FifoOrderBook(LimitOrders)
        new_order = LimitOrder(ID=3, price=99, volume=2, buy=False, creation_time=datetime.now())
        trades = limit_order_book.limit_order_sell(new_order)
        assert len(trades) == 2
        assert limit_order_book.bid.qsize() == 1
        bid_max = limit_order_book.bid.get(timeout=0.1)
        assert bid_max.price == 100
        assert bid_max.volume == 1

    def test_partial_limit_sell_order(self):
        LimitOrders = [
            LimitOrder(ID=0, price=102, volume=1, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=1, price=101, volume=2, buy=True, creation_time=datetime.now()),
            LimitOrder(ID=2, price=100, volume=1, buy=True, creation_time=datetime.now()),
        ]
        limit_order_book = FifoOrderBook(LimitOrders)
        new_order = LimitOrder(ID=3, price=101, volume=2, buy=False, creation_time=datetime.now())
        trades = limit_order_book.limit_order_sell(new_order)
        assert len(trades) == 2
        assert limit_order_book.bid.qsize() == 2
        bid_max = limit_order_book.bid.get(timeout=0.1)
        assert bid_max.price == 101
        assert bid_max.volume == 1