from django.db import transaction
from core.models import Order, OrderItem, Product, Supplier, OrderStatus
from core.repositories.order_repository import OrderRepository

class OrderService:

    def __init__(self):
        self.repo = OrderRepository()

    @transaction.atomic
    def create_order(self, dto):
        supplier = Supplier.objects.get(id=dto.supplier_id)

        order = Order.objects.create(
            supplier=supplier,
            status=OrderStatus.PENDING.value
        )

        for item in dto.items:
            product = Product.objects.get(id=item.product_id)

            if item.quantity <= 0:
                raise ValueError("Quantity must be greater than 0")

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.advised_price,
            )

        return order

    @transaction.atomic
    def receive_order(self, order_id):
        order = (
            Order.objects
            .select_for_update()
            .prefetch_related("items__product")
            .get(id=order_id)
        )

        if order.status != OrderStatus.PENDING.value:
            raise ValueError("Only pending orders can be received")

        for item in order.items.all():
            product = Product.objects.select_for_update().get(id=item.product.id)
            product.stock_quantity += item.quantity
            product.save()

        order.status = OrderStatus.RECEIVED.value
        order.save()

        return order

    def get_orders(self):
        return self.repo.get_all_orders()

    def get_order(self, order_id):
        return Order.objects.prefetch_related(
            "items__product", "supplier"
        ).get(id=order_id)

