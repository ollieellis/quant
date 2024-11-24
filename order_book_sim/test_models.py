from datetime import datetime, timedelta
from models import LimitOrder, MarketOrder, StopLimit, StopOrder

class TestComparisonOperators:
    def testBuyBiggerLessThan(self):
        now = datetime.now()
        o1 =  LimitOrder(ID=1, price=100, volume=1, buy=True, creation_time=now)
        o2 =  LimitOrder(ID=1, price=99, volume=1, buy=True, creation_time=now)
        assert o1 < o2 #needs to be smaller for the priority que

    def testSellBiggerBiggerThan(self):
        now = datetime.now()
        o1 =  LimitOrder(ID=1, price=100, volume=1, buy=False, creation_time=now)
        o2 =  LimitOrder(ID=1, price=99, volume=1, buy=False, creation_time=now)
        assert o2 < o1 #needs to be smaller for the priority que

    def testBuyNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 =  LimitOrder(ID=1, price=100, volume=1, buy=True, creation_time=earlier)
        o2 =  LimitOrder(ID=1, price=100, volume=1, buy=True, creation_time=now)
        assert o1 < o2 #needs to be smaller for the priority que

    def testSellNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 =  LimitOrder(ID=1, price=100, volume=1, buy=False, creation_time=earlier)
        o2 =  LimitOrder(ID=1, price=100, volume=1, buy=False, creation_time=now)
        assert o1 < o2 #needs to be smaller for the priority que

    def testBuyBiggerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 =  LimitOrder(ID=1, price=100, volume=1, buy=True, creation_time=now)
        o2 =  LimitOrder(ID=1, price=99, volume=1, buy=True, creation_time=earlier)
        assert o1 < o2 #needs to be smaller for the priority que


    def testSellLowerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 =  LimitOrder(ID=1, price=100, volume=1, buy=False, creation_time=now)
        o2 =  LimitOrder(ID=1, price=101, volume=1, buy=False, creation_time=earlier)
        assert o1 < o2 #needs to be smaller for the priority que

market_order = MarketOrder(volume=1, buy=True)
limit_order = LimitOrder(price=20, volume=1, buy=True)

class TestStopOrderComparisonOperators:
    def testBuyBiggerLessThan(self):
        now = datetime.now()
        o1 = StopOrder(ID=1, trigger_price=100, trigger_above=True, creation_time=now, order=market_order)
        o2 = StopOrder(ID=2, trigger_price=99, trigger_above=True, creation_time=now, order=market_order)
        assert o1 > o2  # Higher buy trigger price should be smaller in priority queue

    def testSellBiggerBiggerThan(self):
        now = datetime.now()
        o1 = StopOrder(ID=1, trigger_price=100, trigger_above=False, creation_time=now, order=market_order)
        o2 = StopOrder(ID=2, trigger_price=99, trigger_above=False, creation_time=now, order=market_order)
        assert o1 < o2  # Lower sell trigger price should be smaller in priority queue

    def testBuyNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopOrder(ID=1, trigger_price=100, trigger_above=True, creation_time=earlier, order=market_order)
        o2 = StopOrder(ID=2, trigger_price=100, trigger_above=True, creation_time=now, order=market_order)
        assert o1 < o2  # Older buy trigger price should be smaller in priority queue

    def testSellNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopOrder(ID=1, trigger_price=100, trigger_above=False, creation_time=earlier, order=market_order)
        o2 = StopOrder(ID=2, trigger_price=100, trigger_above=False, creation_time=now, order=market_order)
        assert o1 < o2  # Older sell trigger price should be smaller in priority queue

    def testBuyBiggerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopOrder(ID=1, trigger_price=100, trigger_above=True, creation_time=now, order=market_order)
        o2 = StopOrder(ID=2, trigger_price=99, trigger_above=True, creation_time=earlier, order=market_order)
        assert o2 < o1  # Higher buy trigger price with newer timestamp should be smaller

    def testSellLowerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopOrder(ID=1, trigger_price=100, trigger_above=False, creation_time=now, order=market_order)
        o2 = StopOrder(ID=2, trigger_price=101, trigger_above=False, creation_time=earlier, order=market_order)
        assert o2 < o1  # Lower sell trigger price with newer timestamp should be smaller


class TestStopLimitComparisonOperators:
    def testBuyBiggerLessThan(self):
        now = datetime.now()
        o1 = StopLimit(ID=1, trigger_price=100, trigger_above=True, creation_time=now, order=limit_order)
        o2 = StopLimit(ID=2, trigger_price=99, trigger_above=True, creation_time=now, order=limit_order)
        assert o2 < o1  # Higher buy trigger price should be smaller in priority queue

    def testSellBiggerBiggerThan(self):
        now = datetime.now()
        o1 = StopLimit(ID=1, trigger_price=100, trigger_above=False, creation_time=now, order=limit_order)
        o2 = StopLimit(ID=2, trigger_price=99, trigger_above=False, creation_time=now, order=limit_order)
        assert o2 > o1  # Lower sell trigger price should be smaller in priority queue

    def testBuyNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopLimit(ID=1, trigger_price=100, trigger_above=True, creation_time=earlier, order=limit_order)
        o2 = StopLimit(ID=2, trigger_price=100, trigger_above=True, creation_time=now, order=limit_order)
        assert o1 < o2  # Older buy trigger price should be smaller in priority queue

    def testSellNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopLimit(ID=1, trigger_price=100, trigger_above=False, creation_time=earlier, order=limit_order)
        o2 = StopLimit(ID=2, trigger_price=100, trigger_above=False, creation_time=now, order=limit_order)
        assert o1 < o2  # Older sell trigger price should be smaller in priority queue

    def testBuyBiggerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopLimit(ID=1, trigger_price=100, trigger_above=True, creation_time=now, order=limit_order)
        o2 = StopLimit(ID=2, trigger_price=99, trigger_above=True, creation_time=earlier, order=limit_order)
        assert o1 > o2  # Higher buy trigger price with newer timestamp should be smaller

    def testSellLowerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = StopLimit(ID=1, trigger_price=100, trigger_above=False, creation_time=now, order=limit_order)
        o2 = StopLimit(ID=2, trigger_price=101, trigger_above=False, creation_time=earlier, order=limit_order)
        assert o1 > o2  # Lower sell trigger price with newer timestamp should be smaller

class TestStopOrderVsStopLimitComparison:
    def testBuyOrderVsLimitHigherTrigger(self):
        now = datetime.now()
        order = StopOrder(ID=1, trigger_price=100, trigger_above=True, creation_time=now, order=market_order)
        limit = StopLimit(ID=2, trigger_price=99, trigger_above=True, creation_time=now, order=limit_order)
        assert order > limit

    def testSellOrderVsLimitLowerTrigger(self):
        now = datetime.now()
        order = StopOrder(ID=1, trigger_price=100, trigger_above=False, creation_time=now, order=market_order)
        limit = StopLimit(ID=2, trigger_price=101, trigger_above=False, creation_time=now, order=limit_order)
        assert limit < order

    def testBuyOrderVsLimitSameTriggerOlderOrder(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        order = StopOrder(ID=1, trigger_price=100, trigger_above=True, creation_time=earlier, order=market_order)
        limit = StopLimit(ID=2, trigger_price=100, trigger_above=True, creation_time=now, order=limit_order)
        assert order < limit

    def testSellOrderVsLimitSameTriggerOlderLimit(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        order = StopOrder(ID=1, trigger_price=100, trigger_above=False, creation_time=now, order=market_order)
        limit = StopLimit(ID=2, trigger_price=100, trigger_above=False, creation_time=earlier, order=limit_order)
        assert limit < order

    def testBuyOrderVsLimitNewerOrder(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        order = StopOrder(ID=1, trigger_price=100, trigger_above=True, creation_time=now, order=market_order)
        limit = StopLimit(ID=2, trigger_price=101, trigger_above=True, creation_time=earlier, order=limit_order)
        assert limit > order

    def testSellOrderVsLimitNewerLimit(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        order = StopOrder(ID=1, trigger_price=99, trigger_above=False, creation_time=earlier, order=market_order)
        limit = StopLimit(ID=2, trigger_price=100, trigger_above=False, creation_time=now, order=limit_order)
        assert order > limit