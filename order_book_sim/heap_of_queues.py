# from typing import Optional, List
# import heapq

# from models import Order

# class HeadOfQueues:

#     def __init__(self, orders: Optional[List[Order]]=None):
#         self.q_map = {}
#         self.heap = []
#         for o in orders:
#             self.push(o)

#     def push(self, order: Order):
#         price = order.price
#         if price in self.q_map:
#             self.q_map[price].append(order)
#         que = [order]
#         self.q_map = que
#         heapq.push(self.heap, price)

#     def pop(self, volume: int, price: float):
#         price = self.heap[0]
#         que = self.q_map[price]
#         while volume:
#             if que[0].volume <= volume:
#                 volume -= que[0].volume
#                 que.pop(0)

#     def __drain_que(self, volume: int) -> bool:
#         """given a list"""
#THINK USING A PRIORITY QUE; where we rank each order both of time and price is more elegent