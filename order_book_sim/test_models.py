from datetime import datetime, timedelta
from models import *

class TestComparisonOperators:
    def testBuyBiggerLessThan(self):
        now = datetime.now()
        o1 = LimitOrderBuy(price=100, volume=1, creation_time=now)
        o2 = LimitOrderBuy(price=99, volume=1, creation_time=now)
        assert o1 < o2  # Needs to be smaller for the priority queue

    def testSellBiggerBiggerThan(self):
        now = datetime.now()
        o1 = LimitOrderSell(price=100, volume=1, creation_time=now)
        o2 = LimitOrderSell(price=99, volume=1, creation_time=now)
        assert o2 < o1  # Needs to be smaller for the priority queue

    def testBuyNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = LimitOrderBuy(price=100, volume=1, creation_time=earlier)
        o2 = LimitOrderBuy(price=100, volume=1, creation_time=now)
        assert o1 < o2  # Needs to be smaller for the priority queue

    def testSellNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = LimitOrderSell(price=100, volume=1, creation_time=earlier)
        o2 = LimitOrderSell(price=100, volume=1, creation_time=now)
        assert o1 < o2  # Needs to be smaller for the priority queue

    def testBuyBiggerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = LimitOrderBuy(price=100, volume=1, creation_time=now)
        o2 = LimitOrderBuy(price=99, volume=1, creation_time=earlier)
        assert o1 < o2  # Needs to be smaller for the priority queue

    def testSellLowerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        o1 = LimitOrderSell(price=100, volume=1, creation_time=now)
        o2 = LimitOrderSell(price=101, volume=1, creation_time=earlier)
        assert o1 < o2  # Needs to be smaller for the priority queue


market_order = MarketOrderBuy(volume=1, buy=True)
limit_order = LimitOrderBuy(price=20, volume=1, buy=True)

class TestStopOrderComparisonOperators:
    def testBuyBiggerLessThan(self):
        now = datetime.now()
        market_order = MarketOrderBuy(volume=1)
        o1 = StopOrderTriggerAbove(trigger_price=100, creation_time=now, order=market_order)
        o2 = StopOrderTriggerAbove(trigger_price=99, creation_time=now, order=market_order)
        assert o1 > o2  # Higher buy trigger price should be smaller in priority queue

    def testSellBiggerBiggerThan(self):
        now = datetime.now()
        market_order = MarketOrderBuy(volume=1)
        o1 = StopOrderTriggerBelow(trigger_price=100, creation_time=now, order=market_order)
        o2 = StopOrderTriggerBelow(trigger_price=99, creation_time=now, order=market_order)
        assert o1 < o2  # Lower sell trigger price should be smaller in priority queue

    def testBuyNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        o1 = StopOrderTriggerAbove(trigger_price=100, creation_time=earlier, order=market_order)
        o2 = StopOrderTriggerAbove(trigger_price=100, creation_time=now, order=market_order)
        assert o1 < o2  # Older buy trigger price should be smaller in priority queue

    def testSellNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        o1 = StopOrderTriggerBelow(trigger_price=100, creation_time=earlier, order=market_order)
        o2 = StopOrderTriggerBelow(trigger_price=100, creation_time=now, order=market_order)
        assert o1 < o2  # Older sell trigger price should be smaller in priority queue

    def testBuyBiggerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        o1 = StopOrderTriggerAbove(trigger_price=100, creation_time=now, order=market_order)
        o2 = StopOrderTriggerAbove(trigger_price=99, creation_time=earlier, order=market_order)
        assert o2 < o1  # Higher buy trigger price with newer timestamp should be smaller

    def testSellLowerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        o1 = StopOrderTriggerBelow(trigger_price=100, creation_time=now, order=market_order)
        o2 = StopOrderTriggerBelow(trigger_price=101, creation_time=earlier, order=market_order)
        assert o2 < o1  # Lower sell trigger price with newer timestamp should be smaller


class TestStopLimitComparisonOperators:
    def testBuyBiggerLessThan(self):
        now = datetime.now()
        limit_order = LimitOrderBuy(price=20, volume=1)
        o1 = StopLimitTriggerAbove(trigger_price=100, creation_time=now, order=limit_order)
        o2 = StopLimitTriggerAbove(trigger_price=99, creation_time=now, order=limit_order)
        assert o2 < o1  # Higher buy trigger price should be smaller in priority queue

    def testSellBiggerBiggerThan(self):
        now = datetime.now()
        limit_order = LimitOrderBuy(price=20, volume=1)
        o1 = StopLimitTriggerBelow(trigger_price=100, creation_time=now, order=limit_order)
        o2 = StopLimitTriggerBelow(trigger_price=99, creation_time=now, order=limit_order)
        assert o2 > o1  # Lower sell trigger price should be smaller in priority queue

    def testBuyNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        limit_order = LimitOrderBuy(price=20, volume=1)
        o1 = StopLimitTriggerAbove(trigger_price=100, creation_time=earlier, order=limit_order)
        o2 = StopLimitTriggerAbove(trigger_price=100, creation_time=now, order=limit_order)
        assert o1 < o2  # Older buy trigger price should be smaller in priority queue

    def testSellNewerLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        limit_order = LimitOrderBuy(price=20, volume=1)
        o1 = StopLimitTriggerBelow(trigger_price=100, creation_time=earlier, order=limit_order)
        o2 = StopLimitTriggerBelow(trigger_price=100, creation_time=now, order=limit_order)
        assert o1 < o2  # Older sell trigger price should be smaller in priority queue

    def testBuyBiggerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        limit_order = LimitOrderBuy(price=20, volume=1)
        o1 = StopLimitTriggerAbove(trigger_price=100, creation_time=now, order=limit_order)
        o2 = StopLimitTriggerAbove(trigger_price=99, creation_time=earlier, order=limit_order)
        assert o1 > o2  # Higher buy trigger price with newer timestamp should be smaller

    def testSellLowerOrderLessThan(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        limit_order = LimitOrderBuy(price=20, volume=1)
        o1 = StopLimitTriggerBelow(trigger_price=100, creation_time=now, order=limit_order)
        o2 = StopLimitTriggerBelow(trigger_price=101, creation_time=earlier, order=limit_order)
        assert o1 > o2  # Lower sell trigger price with newer timestamp should be smaller


class TestStopOrderVsStopLimitComparison:
    def testBuyOrderVsLimitHigherTrigger(self):
        now = datetime.now()
        market_order = MarketOrderBuy(volume=1)
        limit_order = LimitOrderBuy(price=20, volume=1)
        order = StopOrderTriggerAbove(trigger_price=100, creation_time=now, order=market_order)
        limit = StopLimitTriggerAbove(trigger_price=99, creation_time=now, order=limit_order)
        assert order > limit  # Higher trigger price buy order should have lower priority

    def testSellOrderVsLimitLowerTrigger(self):
        now = datetime.now()
        market_order = MarketOrderBuy(volume=1)
        limit_order = LimitOrderBuy(price=20, volume=1)
        order = StopOrderTriggerBelow(trigger_price=100, creation_time=now, order=market_order)
        limit = StopLimitTriggerBelow(trigger_price=101, creation_time=now, order=limit_order)
        assert limit < order  # Lower trigger price sell limit should have higher priority

    def testBuyOrderVsLimitSameTriggerOlderOrder(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        limit_order = LimitOrderBuy(price=20, volume=1)
        order = StopOrderTriggerAbove(trigger_price=100, creation_time=earlier, order=market_order)
        limit = StopLimitTriggerAbove(trigger_price=100, creation_time=now, order=limit_order)
        assert order < limit  # Older buy order should have higher priority for same trigger price

    def testSellOrderVsLimitSameTriggerOlderLimit(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        limit_order = LimitOrderBuy(price=20, volume=1)
        order = StopOrderTriggerBelow(trigger_price=100, creation_time=now, order=market_order)
        limit = StopLimitTriggerBelow(trigger_price=100, creation_time=earlier, order=limit_order)
        assert limit < order  # Older sell limit should have higher priority for same trigger price

    def testBuyOrderVsLimitNewerOrder(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        limit_order = LimitOrderBuy(price=20, volume=1)
        order = StopOrderTriggerAbove(trigger_price=100, creation_time=now, order=market_order)
        limit = StopLimitTriggerAbove(trigger_price=101, creation_time=earlier, order=limit_order)
        assert limit > order  # Higher trigger price with older creation time should have lower priority

    def testSellOrderVsLimitNewerLimit(self):
        now = datetime.now()
        earlier = now - timedelta(seconds=0.01)
        market_order = MarketOrderBuy(volume=1)
        limit_order = LimitOrderBuy(price=20, volume=1)
        order = StopOrderTriggerBelow(trigger_price=99, creation_time=earlier, order=market_order)
        limit = StopLimitTriggerBelow(trigger_price=100, creation_time=now, order=limit_order)
        assert order > limit  # Lower trigger price with newer creation time should have higher priority