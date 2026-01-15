# core/views/order_view.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.dto.order_dto import OrderDTO, OrderItemDTO
from core.models import Order, OrderItem
from core.permissions import IsStaffOrAdmin
from core.repositories.order_repository import OrderRepository
from core.repositories.product_repository import ProductRepository
from core.repositories.supplier_repository import SupplierRepository
from core.services.order_service import OrderService


def get_order_service():
    return OrderService(
        repo=OrderRepository(),
        product_repo=ProductRepository(),
        supplier_repo=SupplierRepository(),
        order_model=Order,
        order_item_model=OrderItem,
    )


@require_POST
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

    dto = OrderDTO(supplier_id=data["supplier_id"], status="pending", items=items)

    service = get_order_service()
    order = service.create_order(dto)

    return JsonResponse({"message": "Order created", "order_id": order.id}, status=201)


@require_GET
@api_view(["GET"])
@permission_classes([AllowAny])
def get_orders(request):
    service = get_order_service()
    orders = service.get_orders()

    response = []
    for order in orders:
        response.append(
            {
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
                ],
            }
        )

    return JsonResponse(response, safe=False)


@require_POST
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsStaffOrAdmin])
def receive_order(request, order_id):
    service = get_order_service()

    try:
        order = service.receive_order(order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"message": "Order received", "order_id": order.id})


@require_GET
@api_view(["GET"])
@permission_classes([AllowAny])
def get_order(request, order_id):
    service = get_order_service()
    order = service.get_order(order_id)

    return JsonResponse(
        {
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
            ],
        }
    )
