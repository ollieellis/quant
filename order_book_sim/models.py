from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional, Union
import uuid

#marketOrder: just fullfill me at best price rn
#limit bid/ask
#stop market; once last traded stock hits price initiate a market order
#stop limit: once last traded stock hits price initiate a limit order

class MarketOrder(BaseModel):
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    volume: int
    buy: bool
    creation_time: datetime = Field(default_factory=datetime.now)

class LimitOrder(BaseModel):
    ID: int = uuid.uuid4()
    price: float
    volume: int  # for this sim we will only trade whole securitys
    buy: bool
    creation_time: datetime=datetime.now()

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
    

class StopBase(BaseModel):
    ID: int = uuid.uuid4()
    trigger_price: float
    trigger_above: bool
    creation_time: datetime

    def __lt__(self, other):
        # if not isinstance(other, (StopOrder, StopLimit)):
        #     return NotImplemented
        if self.trigger_above:
            return self.less_than(other)
        else:
            return self.greater_than(other)

    def __gt__(self, other):
        # if not isinstance(other, (StopOrder, StopLimit)):
        #     return NotImplemented
        if self.trigger_above:
            return self.greater_than(other)
        else:
            return self.less_than(other)

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other
    
    def less_than(self, other):
        if self.trigger_price < other.trigger_price:
            return True
        if self.trigger_price == other.trigger_price:
            return self.creation_time < other.creation_time
        return False
    
    def greater_than(self, other):
        if self.trigger_price > other.trigger_price:
            return True
        if self.trigger_price == other.trigger_price:
            return self.creation_time < other.creation_time
        return False

class StopOrder(StopBase):
    order: MarketOrder

class StopLimit(StopBase):
    order: LimitOrder 


class Cancelation:
    ID: int
    creation_time: datetime
    
Order = Union[MarketOrder, LimitOrder, StopOrder, StopLimit, Cancelation]