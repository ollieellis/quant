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
    
    def market_buy(self, volume: int) -> List[LimitOrder]:
        pass
    
    def initialize_heaps(self, orders: Optional[List[LimitOrder]]):
        for o in orders:
            if o.buy:
                self.limit_order_buy(o)
            else:
                self.limit_order_sell(o)
    
    # def limit_order_buy(volume: int, price: float): 
    def limit_order_buy(self, order: LimitOrder):
        if self.ask.qsize() == 0:
            self.bid.put(order)
            return []
        
        ask_min = self.ask.get()
        if order.price < ask_min.price:
            self.bid.put(order)
            self.ask.put(ask_min)
        
        volume = order.volume
        orders_to_complete = []
        while (order.price > ask_min.price) and (volume > 0):
            if volume >= ask_min.volume:
                orders_to_complete.append(ask_min)
                volume - ask_min.volume
                ask_min = self.ask.get() #here we will block if we dont have the other side to fill the order
            if volume < ask_min.volume:
                partial_ask = ask_min.copy(deep=True)
                partial_ask.volume = volume
                orders_to_complete.append(partial_ask)
                ask_min.volume -= volume
                self.ask.put(ask_min)
            
    def limit_order_sell(self, order):
        if self.bid.qsize() == 0:
            self.ask.put(order)
            return []
        
        bid_max = self.ask.get()
        if order.price > bid_max.price:
            self.ask.put(order)
            self.bid.put(bid_max)
        
        volume = order.volume
        orders_to_complete = []
        while (order.price < bid_max.price) and (volume > 0):
            if volume >= bid_max.volume:
                orders_to_complete.append(bid_max)
                volume - bid_max.volume
                bid_max = self.bid.get()
            if volume < bid_max.volume:
                partial_ask = bid_max.copy(deep=True)
                partial_ask.volume = volume
                orders_to_complete.append(partial_ask)
                bid_max.volume -= volume
                self.ask.put(bid_max)
