import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.dto.order_dto import OrderDTO, OrderItemDTO
from core.services.order_service import OrderService
from core.models import Order

@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    if "supplier_id" not in data or "items" not in data:
        return JsonResponse({"error": "supplier_id and items required"}, status=400)

    items = [
        OrderItemDTO(
            product_id=i["product_id"],
            quantity=i["quantity"],
        )
        for i in data["items"]
    ]

    dto = OrderDTO(
        supplier_id=data["supplier_id"],
        status="pending",
        items=items
    )

    order = OrderService().create_order(dto)
    return JsonResponse({"message": "Order created", "order_id": order.id}, status=201)



@csrf_exempt
def get_orders(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

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
                    "price": float(item.price),
                }
                for item in order.items.all()
            ]
        })

    return JsonResponse(response, safe=False)


@csrf_exempt
def receive_order(request, order_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    service = OrderService()
    try:
        order = service.receive_order(order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": "Server error: " + str(e)}, status=500)

    return JsonResponse({"message": "Order received", "order_id": order.id})


@csrf_exempt
def get_order(request, order_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    order = OrderService().get_order(order_id)

    return JsonResponse({
        "id": order.id,
        "supplier": order.supplier.name,
        "status": order.status,
        "created_at": str(order.created_at),
        "items": [
            {
                "product": item.product.name,
                "quantity": item.quantity,
            }
            for item in order.items.all()
        ]
    })
