from django.http import JsonResponse
from core.models import Supplier

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def supplier_list(request):
    suppliers = Supplier.objects.all()
    data = [{"id": s.id, "name": s.name} for s in suppliers]
    return JsonResponse(data, safe=False)

