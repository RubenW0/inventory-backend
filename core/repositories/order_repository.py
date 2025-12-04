from core.models import Order, OrderItem

class OrderRepository:

    def create_order(self, order_dto):
        order = Order.objects.create(
            supplier_id=order_dto.supplier_id,
            status=order_dto.status,
        )

        for item in order_dto.items:
            OrderItem.objects.create(
                order=order,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )

        return order


    def get_all_orders(self):
        return Order.objects.prefetch_related("items", "supplier").all()
