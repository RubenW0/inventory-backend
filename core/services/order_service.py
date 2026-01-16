# core/services/order_service.py
from core.models import OrderStatus


class OrderService:
    def __init__(
        self, repo, product_repo, supplier_repo, order_model, order_item_model
    ):
        self.repo = repo
        self.product_repo = product_repo
        self.supplier_repo = supplier_repo
        self.order_model = order_model
        self.order_item_model = order_item_model

    def create_order(self, dto):
        supplier = self.supplier_repo.get(dto.supplier_id)

        order = self.order_model(supplier=supplier, status=OrderStatus.PENDING.value)
        order.save()

        for item in dto.items:
            product = self.product_repo.get(item.product_id)

            if item.quantity <= 0:
                raise ValueError("Quantity must be greater than 0")

            if hasattr(self.order_item_model, "objects"):
                self.order_item_model.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.advised_price,
                )
            else:
                order.items.append(
                    self.order_item_model(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.advised_price,
                    )
                )

        return order

    def receive_order(self, order_id):
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        if order.status != OrderStatus.PENDING.value:
            raise ValueError("Only pending orders can be received")

        for item in order.items.all():
            item.product.stock_quantity += item.quantity
            item.product.save()

        order.status = OrderStatus.RECEIVED.value
        self.repo.save(order)
        return order

    def get_orders(self):
        return self.repo.get_all_orders()

    def get_order(self, order_id):
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        return order
