# core/repositories/product_repository.py
from core.models import Product
from django.core.exceptions import ObjectDoesNotExist


class ProductRepository:
    def get_all(self):
        return list(Product.objects.all())

    def get_by_id(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return None

    def create(self, dto, total_value, status):
        return Product.objects.create(
            name=dto.name,
            type=dto.type,
            stock_quantity=dto.stock_quantity,
            min_stock=dto.min_stock,
            advised_price=dto.advised_price,
            total_value=total_value,
            location=dto.location,
            status=status
        )

    def save(self, product):
        product.save()
        return product

    def delete(self, product_id):
        product = self.get_by_id(product_id)
        if not product:
            return False
        product.delete()
        return True
