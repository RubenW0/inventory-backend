from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered", "id": user.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
