from django.core.exceptions import ObjectDoesNotExist

from core.models import Order


class OrderRepository:
    def get_all_orders(self):
        return Order.objects.prefetch_related(
            "items", "items__product", "supplier"
        ).all()

    def get_order_by_id(self, order_id):
        try:
            return Order.objects.prefetch_related(
                "items", "items__product", "supplier"
            ).get(id=order_id)
        except ObjectDoesNotExist:
            return None

    def save(self, order):
        order.save()
        return order
