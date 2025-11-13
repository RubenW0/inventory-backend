# core/dtos.py
from dataclasses import dataclass

@dataclass
class ProductDTO:
    id: int
    name: str
    type: str
    stock_quantity: float
    min_stock: int
    advised_price: float
    total_value: float
    location: str
    status: str


@dataclass
class ProductCreateDTO:
    name: str
    type: str
    stock_quantity: float
    min_stock: int
    advised_price: float
    total_value: float
    location: str
    status: str

