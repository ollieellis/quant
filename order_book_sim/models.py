from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, Union

#marketOrder: just fullfill me at best price rn
#limit bid/ask
#stop market; once last traded stock hits price initiate a market order
#stop limit: once last traded stock hits price initiate a limit order

class MarketOrder(BaseModel):
    ID: int
    volume: int
    buy: bool
    creation_time: Optional[datetime]=datetime.now()

class LimitOrder(BaseModel):
    ID: int
    price: float
    volume: int  # for this sim we will only trade whole secs
    buy: bool
    creation_time: datetime

    def __lt__(self, other):
        """Returns the priority needed by the priority Queue. 
        If a buy, the bigger/newer order will be < smaller/older.
        If a sell, lower/newer orders will be less than."""
        if not isinstance(other, LimitOrder):
            return NotImplemented

        if self.buy:
            return self.greater_than(other)
        else:
            return self.less_than(other)

    def __gt__(self, other):
        """Returns the priority needed by the priority Queue.
        If a buy, the bigger/newer order will be > bigger/newer.
        If a sell, higher/older orders will be greater than."""
        if not isinstance(other, LimitOrder):
            return NotImplemented

        if self.buy:
            return self.less_than(other)
        else:
            return self.greater_than(other)

    def __le__(self, other):
        """Returns the priority needed by the priority Queue.
        If a buy, the smaller/newer order will be >= bigger/newer.
        If a sell, higher/older orders will be >= than."""   
        return not self > other

    def __ge__(self, other):
        """Returns the priority needed by the priority Queue.
        If a buy, the smaller/newer order will be <= bigger/newer.
        If a sell, higher/older orders will be >= than."""           
        return not self < other

    def less_than(self, other):
        if self.price < other.price:
            return True
        if self.price == other.price:
            return self.creation_time < other.creation_time
        return False

    def greater_than(self, other):
        if self.price > other.price:
            return True
        if self.price == other.price:
            return self.creation_time < other.creation_time
        return False
    

class StopOrder:
    ID: int
    trigger_price: float
    trigger_above: bool
    creation_time: datetime
    order: MarketOrder #need to make sure the creation times are handled correctly...

class StopLimit:
    ID: int
    trigger_price: float
    trigger_above: bool
    creation_time: datetime
    order: LimitOrder #need to make sure the creation times are handled correctly...
    
    
