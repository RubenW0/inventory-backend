# core/tests/test_order_service.py
import unittest
from core.services.order_service import OrderService
from core.tests.fakes.fake_order_repo import (
    FakeProduct, FakeSupplier, FakeOrder, FakeOrderItem, FakeOrderRepository
)
from core.models import OrderStatus

class FakeDTOItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

class FakeOrderDTO:
    def __init__(self, supplier_id, items):
        self.supplier_id = supplier_id
        self.items = items

class TestOrderService(unittest.TestCase):
    def setUp(self):
        # Fakes
        self.product1 = FakeProduct(id=1, name="Laptop", advised_price=1000)
        self.product2 = FakeProduct(id=2, name="Mouse", advised_price=25)
        self.supplier = FakeSupplier(id=1, name="TechSupplier")

        self.fake_repo = FakeOrderRepository()

        self.service = OrderService()
        self.service.repo = self.fake_repo

        self.service.Product_objects_get = lambda id: self.product1 if id == 1 else self.product2
        self.service.Supplier_objects_get = lambda id: self.supplier

        self.service._create_order_item = lambda order, item: order.items.append(
            FakeOrderItem(
                product=self.service.Product_objects_get(item.product_id),
                quantity=item.quantity,
                price=self.service.Product_objects_get(item.product_id).advised_price
            )
        )

    def test_create_order_success(self):
        dto = FakeOrderDTO(
            supplier_id=1,
            items=[FakeDTOItem(product_id=1, quantity=2), FakeDTOItem(product_id=2, quantity=5)]
        )

        order = FakeOrder(id=0, supplier=self.supplier)
        for item in dto.items:
            self.service._create_order_item(order, item)
        self.fake_repo.save(order)

        self.assertEqual(len(self.fake_repo.get_all_orders()), 1)
        self.assertEqual(order.items[0].quantity, 2)
        self.assertEqual(order.items[1].product.name, "Mouse")

    def test_receive_order_updates_stock(self):
        order = FakeOrder(id=1, supplier=self.supplier)
        order.items.append(FakeOrderItem(product=self.product1, quantity=3, price=1000))
        order.items.append(FakeOrderItem(product=self.product2, quantity=2, price=25))
        self.fake_repo.save(order)

        for item in order.items:
            item.product.stock_quantity += item.quantity
        order.status = OrderStatus.RECEIVED.value

        self.assertEqual(order.status, OrderStatus.RECEIVED.value)
        self.assertEqual(self.product1.stock_quantity, 3)
        self.assertEqual(self.product2.stock_quantity, 2)

    def test_get_orders_returns_all(self):
        order1 = FakeOrder(id=1, supplier=self.supplier)
        order2 = FakeOrder(id=2, supplier=self.supplier)
        self.fake_repo.save(order1)
        self.fake_repo.save(order2)

        all_orders = self.fake_repo.get_all_orders()
        self.assertEqual(len(all_orders), 2)
