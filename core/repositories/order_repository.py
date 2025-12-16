from core.models import Order

class OrderRepository:

    def get_all_orders(self):
        return Order.objects.prefetch_related("items", "items__product", "supplier").all()
