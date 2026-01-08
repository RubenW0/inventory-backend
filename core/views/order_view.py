import json
from django.http import JsonResponse
from core.dto.order_dto import OrderDTO, OrderItemDTO
from core.services.order_service import OrderService
from core.models import Order

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from core.permissions import IsStaffOrAdmin



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsStaffOrAdmin])
def create_order(request):
    data = request.data

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




@api_view(["GET"])
@permission_classes([AllowAny])
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
                    "price": float(item.price),
                }
                for item in order.items.all()
            ]
        })

    return JsonResponse(response, safe=False)



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsStaffOrAdmin])
def receive_order(request, order_id):
    service = OrderService()
    try:
        order = service.receive_order(order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"message": "Order received", "order_id": order.id})



@api_view(["GET"])
@permission_classes([AllowAny])
def get_order(request, order_id):
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

