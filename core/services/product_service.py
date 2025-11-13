from core.dto.product_dto import ProductDTO, ProductCreateDTO


class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def list_products(self):
        products = self.repo.get_all()
        return [
            ProductDTO(
                id=p.id,
                name=p.name,
                type=p.type,
                stock_quantity=float(p.stock_quantity),
                min_stock=p.min_stock,
                advised_price=float(p.advised_price),
                total_value=float(p.total_value),
                location=p.location,
                status=p.status
            )
            for p in products
        ]

    def get_product(self, product_id):
        p = self.repo.get_by_id(product_id)
        if not p:
            return None
        return ProductDTO(
            id=p.id,
            name=p.name,
            type=p.type,
            stock_quantity=float(p.stock_quantity),
            min_stock=p.min_stock,
            advised_price=float(p.advised_price),
            total_value=float(p.total_value),
            location=p.location,
            status=p.status
        )

    def create_product(self, dto: ProductCreateDTO):
        product = self.repo.create(dto)
        return ProductDTO(
            id=product.id,
            name=product.name,
            type=product.type,
            stock_quantity=float(product.stock_quantity),
            min_stock=product.min_stock,
            advised_price=float(product.advised_price),
            total_value=float(product.total_value),
            location=product.location,
            status=product.status
        )

    def update_product(self, product_id, **kwargs):
        return self.repo.update(product_id, **kwargs)

    def delete_product(self, product_id):
        return self.repo.delete(product_id)
