# core/tests/fakes/fake_order_repo.py
from core.models import OrderStatus

class FakeProduct:
    def __init__(self, id, name, advised_price, stock_quantity=0):
        self.id = id
        self.name = name
        self.advised_price = advised_price
        self.stock_quantity = stock_quantity

class FakeSupplier:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class FakeOrderItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

class FakeOrder:
    def __init__(self, id, supplier, status=OrderStatus.PENDING.value):
        self.id = id
        self.supplier = supplier
        self.status = status
        self.items = []

class FakeOrderRepository:
    def __init__(self):
        self.orders = []
        self._next_id = 1

    def get_all_orders(self):
        return self.orders

    def save(self, order):
        if order not in self.orders:
            order.id = self._next_id
            self._next_id += 1
            self.orders.append(order)
        return order

    def get_order_by_id(self, order_id):
        return next((o for o in self.orders if o.id == order_id), None)
