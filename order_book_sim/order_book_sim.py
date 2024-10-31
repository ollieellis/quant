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

from models import Order
from order_book import OrderBook

class FifoOrderBook(OrderBook):
    """Price Time Priority matching algo (FIFO)"""

    def __init__(self, orders: Optional[List[Order]]) -> None:
        super().__init__()
        self.bid = PriorityQueue() 
        self.ask = PriorityQueue()
        self.cancels = set()
        self.volumes = {}

    def order(self, order):
        pass

    def cancel(self, order_id: int):
        pass
    
    def snapshot(self):
        return super().snapshot()
    
    def market_buy(volume: int) -> List[Order]:
        pass

    # def limit_order_buy(volume: int, price: float): 
    def limit_order_buy(self, order: Order):
        if self.ask.qsize == 0:
            self.bid.put(order)
        
        ask_min = self.ask.get()
        if order.price < ask_min.price:
            self.bid.put(order)
            self.ask.put(ask_min)
        
        volume = order.volume
        orders_to_complete = []
        while (order.price > ask_min.price) and (volume > 0):
            if volume > ask_min:
                pass
