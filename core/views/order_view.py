import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.dto.order_dto import OrderDTO, OrderItemDTO
from core.services.order_service import OrderService

@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    items = [
        OrderItemDTO(
            product_id=i["product_id"],
            quantity=i["quantity"],
            price=i.get("price", 0)
        )
        for i in data["items"]
    ]

    dto = OrderDTO(
        supplier_id=data["supplier_id"],
        status=data.get("status", "pending"),
        items=items
    )

    order = OrderService().create_order(dto)
    return JsonResponse({"message": "Order created", "order_id": order.id}, status=201)


@csrf_exempt
def get_orders(request):
    orders = OrderService().get_orders()

    response = []
    for order in orders:
        response.append({
            "id": order.id,
            "supplier": order.supplier.name,
            "status": order.status,
            "created_at": str(order.created_at),
            "items": [
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": float(item.price)
                }
                for item in order.items.all()
            ]
        })

    return JsonResponse(response, safe=False)
