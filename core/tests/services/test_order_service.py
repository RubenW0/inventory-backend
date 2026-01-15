# core/tests/test_order_service.py
import unittest

from core.models import OrderStatus
from core.services.order_service import OrderService
from core.tests.fakes.fake_order_repo import (
    FakeOrder,
    FakeOrderItem,
    FakeOrderRepository,
    FakeProduct,
    FakeSupplier,
)


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
        self.product1 = FakeProduct(id=1, name="Laptop", advised_price=1000)
        self.product2 = FakeProduct(id=2, name="Mouse", advised_price=25)
        self.supplier = FakeSupplier(id=1, name="TechSupplier")

        self.fake_repo = FakeOrderRepository()

        self.service = OrderService(
            repo=self.fake_repo,
            product_repo={1: self.product1, 2: self.product2},
            supplier_repo={1: self.supplier},
            order_model=FakeOrder,
            order_item_model=FakeOrderItem,
        )

    def test_create_order_success(self):
        dto = FakeOrderDTO(supplier_id=1, items=[FakeDTOItem(1, 2), FakeDTOItem(2, 5)])

        order = self.service.create_order(dto)

        self.assertEqual(len(order.items), 2)
        self.assertEqual(order.items[0].quantity, 2)
        self.assertEqual(order.items[1].product.name, "Mouse")

    def test_create_order_raises_error_on_zero_quantity(self):
        dto = FakeOrderDTO(1, [FakeDTOItem(1, 0)])
        with self.assertRaises(ValueError):
            self.service.create_order(dto)

    def test_receive_order_updates_stock(self):
        order = FakeOrder(id=1, supplier=self.supplier)
        order.items.append(FakeOrderItem(order, self.product1, 3, 1000))
        order.items.append(FakeOrderItem(order, self.product2, 2, 25))
        self.fake_repo.save(order)

        order.status = OrderStatus.PENDING.value
        self.service.receive_order(order.id)

        self.assertEqual(self.product1.stock_quantity, 3)
        self.assertEqual(self.product2.stock_quantity, 2)

    def test_receive_order_raises_error_if_not_pending(self):
        order = FakeOrder(
            id=1, supplier=self.supplier, status=OrderStatus.RECEIVED.value
        )
        self.fake_repo.save(order)

        with self.assertRaises(ValueError):
            self.service.receive_order(order.id)

    def test_get_orders_returns_all(self):
        self.fake_repo.save(FakeOrder(1, self.supplier))
        self.fake_repo.save(FakeOrder(2, self.supplier))

        result = self.service.get_orders()
        self.assertEqual(len(result), 2)
