from abc import ABC, abstractmethod

class OrderBook(ABC):

    @abstractmethod
    def order(self, order):
        """Place an order in the order book; returns all the orders to be executed"""
        pass

    @abstractmethod
    def cancel(self, order_id):
        """Cancel an order in the order book."""
        pass

    @abstractmethod
    def snapshot(self):
        """Return a snapshot of the current order book state."""
        pass