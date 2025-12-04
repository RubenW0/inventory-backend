from core.repositories.order_repository import OrderRepository

class OrderService:

    def __init__(self):
        self.repo = OrderRepository()

    def create_order(self, order_dto):

        return self.repo.create_order(order_dto)

    def get_orders(self):
        return self.repo.get_all_orders()
