from core.dto.product_dto import ProductCreateDTO, ProductDTO
from core.models import ProductStatus


class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def _determine_product_status(self, stock_quantity: float, min_stock: int) -> str:
        if stock_quantity <= 0:
            return ProductStatus.OUT_OF_STOCK.value
        if stock_quantity <= min_stock:
            return ProductStatus.LOW_STOCK.value
        return ProductStatus.IN_STOCK.value

    def _to_dto(self, product):
        return ProductDTO(
            id=product.id,
            name=product.name,
            type=product.type,
            stock_quantity=float(product.stock_quantity),
            min_stock=product.min_stock,
            advised_price=float(product.advised_price),
            total_value=float(product.total_value),
            location=product.location,
            status=product.status,
        )

    def list_products(self):
        return [self._to_dto(p) for p in self.repo.get_all()]

    def get_product(self, product_id):
        product = self.repo.get_by_id(product_id)
        if not product:
            return None
        return self._to_dto(product)

    def create_product(self, dto: ProductCreateDTO):
        total_value = dto.stock_quantity * dto.advised_price
        status = self._determine_product_status(dto.stock_quantity, dto.min_stock)

        product = self.repo.create(dto, total_value=total_value, status=status)

        return self._to_dto(product)

    def update_product(self, product_id, **kwargs):
        product = self.repo.get_by_id(product_id)
        if not product:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(product, key, value)

        product.total_value = product.stock_quantity * product.advised_price
        product.status = self._determine_product_status(
            product.stock_quantity, product.min_stock
        )

        product = self.repo.save(product)
        return self._to_dto(product)

    def delete_product(self, product_id):
        return self.repo.delete(product_id)
