from dataclasses import dataclass
from typing import List

@dataclass
class OrderItemDTO:
    product_id: int
    quantity: int
    price: float


@dataclass
class OrderDTO:
    supplier_id: int
    status: str
    items: List[OrderItemDTO]
