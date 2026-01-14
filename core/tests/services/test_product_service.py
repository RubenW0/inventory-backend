from unittest import TestCase

from core.services.product_service import ProductService
from core.dto.product_dto import ProductCreateDTO
from core.tests.fakes.fake_product_repo import (
    FakeProduct,
    FakeProductRepository
)
from core.models import ProductStatus


class ProductServiceTests(TestCase):

    def setUp(self):
        self.repo = FakeProductRepository(products=[
            FakeProduct(
                id=1,
                name="Laptop",
                type="Electronics",
                stock_quantity=10,
                min_stock=2,
                advised_price=1000,
                total_value=10000,
                location="A1",
                status=ProductStatus.IN_STOCK.value
            )
        ])
        self.service = ProductService(repo=self.repo)

    def test_list_products_returns_dtos(self):
        products = self.service.list_products()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Laptop")

    def test_get_product_found(self):
        product = self.service.get_product(1)

        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Laptop")

    def test_get_product_not_found(self):
        product = self.service.get_product(999)

        self.assertIsNone(product)

    def test_create_product_sets_total_value_and_status(self):
        dto = ProductCreateDTO(
            name="Mouse",
            type="Electronics",
            stock_quantity=5,
            min_stock=10,
            advised_price=25,
            location="B2"
        )

        product = self.service.create_product(dto)

        self.assertEqual(product.id, 2)
        self.assertEqual(product.total_value, 125.0)
        self.assertEqual(product.status, ProductStatus.LOW_STOCK.value)
        self.assertEqual(len(self.repo.products), 2)

    def test_update_product_recalculates_fields(self):
        updated = self.service.update_product(
            1,
            stock_quantity=0
        )

        self.assertEqual(updated.stock_quantity, 0)
        self.assertEqual(updated.status, ProductStatus.OUT_OF_STOCK.value)
        self.assertEqual(updated.total_value, 0.0)

    def test_delete_product(self):
        result = self.service.delete_product(1)

        self.assertTrue(result)
        self.assertEqual(len(self.repo.products), 0)
