from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator


@method_decorator(require_POST, name="post")
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered", "id": user.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(require_GET, name="get")
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })
