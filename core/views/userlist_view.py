from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers import UserSerializer
from core.permissions import IsAdmin


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all().order_by("id")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UpdateUserRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        new_role = request.data.get("role")

        if new_role not in ["admin", "staff", "employee"]:
            return Response({"error": "Invalid role"}, status=400)

        user.role = new_role
        user.save()

        return Response({"message": "Role updated", "role": new_role})
