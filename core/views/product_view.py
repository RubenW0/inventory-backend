import json
import traceback

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.dto.product_dto import ProductCreateDTO
from core.permissions import IsStaffOrAdmin
from core.repositories.product_repository import ProductRepository
from core.services.product_service import ProductService

service = ProductService(ProductRepository())


@require_GET
@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    try:
        products = service.list_products()
        data = [p.__dict__ for p in products]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse(
            {"error": str(e), "trace": traceback.format_exc()}, status=500
        )


@require_POST
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsStaffOrAdmin])
def product_create(request):
    try:
        print("REQUEST DATA:", request.data)

        data = request.data
        dto = ProductCreateDTO(
            name=data["name"],
            type=data["type"],
            stock_quantity=float(data["stock_quantity"]),
            min_stock=int(data["min_stock"]),
            advised_price=float(data["advised_price"]),
            location=data["location"],
        )
        product = service.create_product(dto)
        return JsonResponse(product.__dict__)

    except (KeyError, ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["PUT"])
@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsStaffOrAdmin])
def product_update(request, product_id):
    try:
        data = request.data

        product = service.update_product(
            product_id=product_id,
            name=data.get("name"),
            type=data.get("type"),
            stock_quantity=data.get("stock_quantity"),
            min_stock=data.get("min_stock"),
            advised_price=data.get("advised_price"),
            location=data.get("location"),
        )

        if not product:
            return HttpResponseBadRequest("Product not found")

        return JsonResponse(
            {
                "id": product.id,
                "name": product.name,
                "type": product.type,
                "stock_quantity": float(product.stock_quantity),
                "min_stock": product.min_stock,
                "advised_price": float(product.advised_price),
                "total_value": float(product.total_value),
                "location": product.location,
                "status": product.status,
            }
        )

    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")
    except Exception as e:
        return JsonResponse(
            {"error": str(e), "trace": traceback.format_exc()}, status=500
        )


@require_http_methods(["DELETE"])
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsStaffOrAdmin])
def product_delete(request, product_id):
    try:
        success = service.delete_product(product_id)
        if success:
            return JsonResponse({"status": "deleted"})
        return HttpResponseBadRequest("Product not found")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
