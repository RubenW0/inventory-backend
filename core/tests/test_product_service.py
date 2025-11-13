# core/tests/test_product_service.py
from unittest import TestCase
from unittest.mock import Mock
from core.services.product_service import ProductService

class ProductServiceTests(TestCase):
    def setUp(self):
        self.mock_repo = Mock()

        self.service = ProductService(repo=self.mock_repo)

    def test_get_product_calls_repository(self):
        # Arrange
        fake_product = {"id": 1, "name": "Toy", "price": 5, "stock": 3}
        self.mock_repo.get_by_id.return_value = fake_product

        # Act
        result = self.service.get_product(1)

        # Assert
        self.mock_repo.get_by_id.assert_called_once_with(1)
        self.assertEqual(result, fake_product)

    def test_create_product_passes_correct_args(self):
        # Arrange
        self.mock_repo.create.return_value = {"id": 2, "name": "Car", "price": 10, "stock": 4}

        # Act
        result = self.service.create_product("Car", 10, 4)

        # Assert
        self.mock_repo.create.assert_called_once_with(name="Car", price=10, stock=4)
        self.assertEqual(result["id"], 2)

    def test_delete_product_returns_repo_value(self):
        # Arrange
        self.mock_repo.delete.return_value = True

        # Act
        result = self.service.delete_product(5)

        # Assert
        self.mock_repo.delete.assert_called_once_with(5)
        self.assertTrue(result)
