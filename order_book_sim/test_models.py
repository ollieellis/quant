from datetime import datetime, timedelta
from models import LimitOrder

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