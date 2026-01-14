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
    def __init__(self, order, product, quantity, price):
        self.order = order
        self.product = product
        self.quantity = quantity
        self.price = price

class FakeOrder:
    def __init__(self, id, supplier, status=OrderStatus.PENDING.value):
        self.id = id
        self.supplier = supplier
        self.status = status
        self.items = []

class FakeProductRepo:
    def __init__(self, products):
        self.products = {p.id: p for p in products}

    def get(self, product_id):
        return self.products[product_id]

class FakeSupplierRepo:
    def __init__(self, suppliers):
        self.suppliers = {s.id: s for s in suppliers}

    def get(self, supplier_id):
        return self.suppliers[supplier_id]

class FakeOrderRepository:
    def __init__(self):
        self.orders = []
        self._next_id = 1

    def save(self, order):
        if order.id is None:
            order.id = self._next_id
            self._next_id += 1
        if order not in self.orders:
            self.orders.append(order)
        return order

    def get_all_orders(self):
        return self.orders

    def get_order_by_id(self, order_id):
        return next((o for o in self.orders if o.id == order_id), None)
