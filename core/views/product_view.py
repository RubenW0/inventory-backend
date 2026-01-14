import json
import traceback
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed

from core.services.product_service import ProductService
from core.repositories.product_repository import ProductRepository
from core.dto.product_dto import ProductCreateDTO

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from core.permissions import IsStaffOrAdmin

service = ProductService(ProductRepository())


@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    try:
        products = service.list_products()
        data = [p.__dict__ for p in products]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e), "trace": traceback.format_exc()}, status=500)



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsStaffOrAdmin])
def product_create(request):
    try:
        data = request.data
        dto = ProductCreateDTO(
            name=data["name"],
            type=data["type"],
            stock_quantity=data["stock_quantity"],
            min_stock=data["min_stock"],
            advised_price=data["advised_price"],
            location=data["location"]
        )
        product = service.create_product(dto)
        return JsonResponse(product.__dict__)
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




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
            location=data.get("location")
        )

        if not product:
            return HttpResponseBadRequest("Product not found")

        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "type": product.type,
            "stock_quantity": float(product.stock_quantity),
            "min_stock": product.min_stock,
            "advised_price": float(product.advised_price),
            "total_value": float(product.total_value),
            "location": product.location,
            "status": product.status
        })

    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")
    except Exception as e:
        return JsonResponse({"error": str(e), "trace": traceback.format_exc()}, status=500)




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

