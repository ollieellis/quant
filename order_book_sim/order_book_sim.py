# the matching algo will be too linked to the implementation of the orderbook
# i will need to make multiple order books for each strat; ie FifoOrderBook(OrderBook)
# as apposed to doing order boox composed of a matching algo
# class MatchingAlgorithm:
#     pass
# class PriceTimePriotity(MatchingAlgorithm):
#     """Price Time Priority matching algo (FIFO)"""
#     pass

from typing import Optional, List, Dict

from queue import PriorityQueue

from models import LimitOrder
from order_book import OrderBook

class FifoOrderBook(OrderBook):
    """Price Time Priority matching algo (FIFO)"""

    def __init__(self, orders: Optional[List[LimitOrder]]) -> None:
        super().__init__()
        self.bid = PriorityQueue() 
        self.ask = PriorityQueue()
        self.cancels = set()
        self.volumes = {}
        self.initialize_heaps(orders)

    def order(self, order):
        pass

    def cancel(self, order_id: int):
        pass
    
    def snapshot(self):
        return super().snapshot()
    
    def initialize_heaps(self, orders: Optional[List[LimitOrder]]):
        for o in orders:
            if o.buy:
                self.limit_order_buy(o)
            else:
                self.limit_order_sell(o)

    def market_buy(self, volume: int) -> List[LimitOrder]:
        """
        Executes a market buy order for a given volume.
        """
        return self.fulfill_buy(float('inf'), volume)

    def market_sell(self, volume: int) -> List[LimitOrder]:
        """
        Executes a market sell order for a given volume.
        """
        return self.fulfill_sell(-float('inf'), volume)

    def limit_order_buy(self, order: LimitOrder):
        """
        Places a limit buy order and tries to fulfill it.
        """
        orders_to_complete = self.fulfill_buy(order.price, order.volume)
        remaining_volume = order.volume - sum(o.volume for o in orders_to_complete)

        if remaining_volume > 0:
            order.volume = remaining_volume
            self.bid.put(order)

        return orders_to_complete

    def limit_order_sell(self, order: LimitOrder):
        """
        Places a limit sell order and tries to fulfill it.
        """
        orders_to_complete = self.fulfill_sell(order.price, order.volume)
        remaining_volume = order.volume - sum(o.volume for o in orders_to_complete)

        if remaining_volume > 0:
            order.volume = remaining_volume
            self.ask.put(order)

        return orders_to_complete
    
  
    def fulfill_buy(self, price: float, volume: int) -> List[LimitOrder]:
        """
        Fulfills a buy order by matching it with the best available asks.
        """
        orders_to_complete = []
        while volume > 0:
            if self.ask.qsize() == 0:
                return orders_to_complete

            ask_min = self.ask.get(timeout=2)

            if price < ask_min.price:
                self.ask.put(ask_min)
                break

            if volume >= ask_min.volume:
                orders_to_complete.append(ask_min)
                volume -= ask_min.volume
            else:
                partial_ask = ask_min.copy(deep=True)
                partial_ask.volume = volume
                orders_to_complete.append(partial_ask)
                ask_min.volume -= volume
                self.ask.put(ask_min)
                volume = 0

        return orders_to_complete

    def fulfill_sell(self, price: float, volume: int) -> List[LimitOrder]:
        """
        Fulfills a sell order by matching it with the best available bids.
        """
        orders_to_complete = []
        while volume > 0:
            if self.bid.qsize() == 0:
                return orders_to_complete

            bid_max = self.bid.get(timeout=2)

            if price > bid_max.price:
                self.bid.put(bid_max)
                break

            if volume >= bid_max.volume:
                orders_to_complete.append(bid_max)
                volume -= bid_max.volume
            else:
                partial_bid = bid_max.copy(deep=True)
                partial_bid.volume = volume
                orders_to_complete.append(partial_bid)
                bid_max.volume -= volume
                self.bid.put(bid_max)
                volume = 0

        return orders_to_complete