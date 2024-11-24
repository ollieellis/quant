from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional, Union
import uuid

#marketOrder: just fullfill me at best price rn
#limit bid/ask
#stop market; once last traded stock hits price initiate a market order
#stop limit: once last traded stock hits price initiate a limit order
#cancel

class MarketOrderBuy(BaseModel):
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    volume: int
    creation_time: datetime = Field(default_factory=datetime.now)

class MarketOrderSell(BaseModel):
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    volume: int
    creation_time: datetime = Field(default_factory=datetime.now)

MarketOrder = Union[MarketOrderBuy, MarketOrderSell]


class LimitOrderBuy(BaseModel):
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    price: float
    volume: int  # for this sim we will only trade whole securitys
    creation_time: datetime = Field(default_factory=datetime.now)

    def __lt__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *bigger* price; then compared by time"""
        if not isinstance(other, LimitOrderBuy):
            return NotImplemented

        if self.price > other.price:
            return True
        if self.price == other.price:
            return self.creation_time < other.creation_time

    def __gt__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *smaller price; then compared by time"""
        if not isinstance(other, LimitOrderBuy):
            return NotImplemented

        if self.price < other.price:
            return True
        if self.price == other.price:
            return self.creation_time < other.creation_time

    def __le__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *bigger* price; then compared by time"""
        return not self > other

    def __ge__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *smaller price; then compared by time"""          
        return not self < other
    

class LimitOrderSell(BaseModel):
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    price: float
    volume: int  # for this sim we will only trade whole securitys
    creation_time: datetime = Field(default_factory=datetime.now)

    def __lt__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *smaller* price; then compared by time"""
        if not isinstance(other, LimitOrderSell):
            return NotImplemented

        if self.price < other.price:
            return True
        if self.price == other.price:
            return self.creation_time < other.creation_time

    def __gt__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *bigger price; then compared by time"""
        if not isinstance(other, LimitOrderSell):
            return NotImplemented

        if self.price > other.price:
            return True
        if self.price == other.price:
            return self.creation_time < other.creation_time

    def __le__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *bigger* price; then compared by time"""
        return not self > other

    def __ge__(self, other):
        """Returns the priority needed by the priority Queue.
        ie will return the *smaller price; then compared by time"""          
        return not self < other

LimitOrder = Union[LimitOrderBuy, LimitOrderSell]


class StopBaseTriggerAbove(BaseModel):
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    trigger_price: float
    creation_time: datetime = Field(default_factory=datetime.now)

    def __lt__(self, other):
        # if not isinstance(other, (StopOrder, StopLimit)):
        #     return NotImplemented
        if self.trigger_price < other.trigger_price:
            return True
        if self.trigger_price == other.trigger_price:
            return self.creation_time < other.creation_time
        return False
    
    def __gt__(self, other):
        # if not isinstance(other, (StopOrder, StopLimit)):
        #     return NotImplemented
        if self.trigger_price > other.trigger_price:
            return True
        if self.trigger_price == other.trigger_price:
            return self.creation_time < other.creation_time
        return False
    
    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other
    
class StopBaseTriggerBelow(BaseModel):
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    trigger_price: float
    creation_time: datetime = Field(default_factory=datetime.now)
    
    def __lt__(self, other):
        # if not isinstance(other, (StopOrder, StopLimit)):
        #     return NotImplemented
        if self.trigger_price > other.trigger_price:
            return True
        if self.trigger_price == other.trigger_price:
            return self.creation_time < other.creation_time
        return False
    
    def __gt__(self, other):
        # if not isinstance(other, (StopOrder, StopLimit)):
        #     return NotImplemented
        if self.trigger_price < other.trigger_price:
            return True
        if self.trigger_price == other.trigger_price:
            return self.creation_time < other.creation_time
        return False
    
    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other

class StopOrderTriggerAbove(StopBaseTriggerAbove):
    order: MarketOrder

class StopOrderTriggerBelow(StopBaseTriggerBelow):
    order: MarketOrder

StopOrder = Union[StopOrderTriggerAbove, StopOrderTriggerBelow]


class StopLimitTriggerAbove(StopBaseTriggerAbove):
    order: LimitOrder 

class StopLimitTriggerBelow(StopBaseTriggerBelow):
    order: LimitOrder

StopLimitOrder = Union[StopLimitTriggerAbove, StopLimitTriggerBelow]

class Cancelation:
    ID: uuid.UUID = Field(default_factory=uuid.uuid4)
    creation_time: datetime = Field(default_factory=datetime.now)
    
Order = Union[MarketOrder, LimitOrder, StopOrder, StopLimitOrder, Cancelation]