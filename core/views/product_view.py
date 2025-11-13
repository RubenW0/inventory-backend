import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from core.services.product_service import ProductService
from core.repositories.product_repository import ProductRepository
from core.dto.product_dto import ProductCreateDTO

service = ProductService(ProductRepository())

@csrf_exempt
def product_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:
        products = service.list_products()
        data = [p.__dict__ for p in products]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e), "trace": traceback.format_exc()}, status=500)


@csrf_exempt
def product_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        data = json.loads(request.body)
        dto = ProductCreateDTO(
            name=data["name"],
            type=data["type"],
            stock_quantity=data["stock_quantity"],
            min_stock=data["min_stock"],
            advised_price=data["advised_price"],
            total_value=data["total_value"],
            location=data["location"],
            status=data["status"]
        )
        product = service.create_product(dto)
        return JsonResponse(product.__dict__)
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def product_update(request, product_id):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"])
    try:
        data = json.loads(request.body)
        product = service.update_product(
            product_id=product_id,
            name=data.get("name"),
            price=data.get("price"),
            stock=data.get("stock")
        )
        if not product:
            return HttpResponseBadRequest("Product not found")
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "stock": product.stock
        })
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def product_delete(request, product_id):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    try:
        success = service.delete_product(product_id)
        if success:
            return JsonResponse({"status": "deleted"})
        return HttpResponseBadRequest("Product not found")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
