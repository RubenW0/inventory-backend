from django.http import JsonResponse
from core.models import Supplier
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def supplier_list(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    suppliers = Supplier.objects.all()
    data = [{"id": s.id, "name": s.name} for s in suppliers]

    return JsonResponse(data, safe=False)
