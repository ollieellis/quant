from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class OrderType(Enum):
    market = 1
    limit = 2
    stop = 3
    stop_limit = 4

class Order(BaseModel):
    ID: int
    price: float
    volume: int #for this sim we will only trade whole secs
    buy: bool
    order_type: OrderType
    creation_time: datetime

    def less_than(self, other):
        if isinstance(other, Order):
            return self.value < other.value
        else:
            return NotImplemented 

    def __lt__(self, other):
        if isinstance(other, Order):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Order):
            return self.value <= other.value
        elif isinstance(other, (int, float)):
            return self.value <= other
        else:
            return NotImplemented
        
    def __gt__(self, other):
        if isinstance(other, Order):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Order):
            return self.value >= other.value
        elif isinstance(other, (int, float)):
            return self.value >= other
        else:
            return NotImplemented 