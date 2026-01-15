# core/tests/fakes/fake_product_repo.py


class FakeProduct:
    def __init__(
        self,
        id,
        name,
        type,
        stock_quantity,
        min_stock,
        advised_price,
        total_value,
        location,
        status,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.stock_quantity = stock_quantity
        self.min_stock = min_stock
        self.advised_price = advised_price
        self.total_value = total_value
        self.location = location
        self.status = status


class FakeProductRepository:
    def __init__(self, products=None):
        self.products = products or []
        self._next_id = len(self.products) + 1

    def get_all(self):
        return self.products

    def get_by_id(self, product_id):
        return next((p for p in self.products if p.id == product_id), None)

    def create(self, dto, total_value, status):
        product = FakeProduct(
            id=self._next_id,
            name=dto.name,
            type=dto.type,
            stock_quantity=dto.stock_quantity,
            min_stock=dto.min_stock,
            advised_price=dto.advised_price,
            total_value=total_value,
            location=dto.location,
            status=status,
        )
        self.products.append(product)
        self._next_id += 1
        return product

    def save(self, product):
        return product

    def delete(self, product_id):
        product = self.get_by_id(product_id)
        if not product:
            return False
        self.products.remove(product)
        return True
