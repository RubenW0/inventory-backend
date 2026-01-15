from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views.auth_view import MeView, RegisterView
from core.views.order_view import create_order, get_order, get_orders, receive_order
from core.views.product_view import (
    product_create,
    product_delete,
    product_list,
    product_update,
)
from core.views.supplier_view import supplier_list

urlpatterns = [
    path("products/", product_list, name="product_list"),
    path("products/create/", product_create, name="product_create"),
    path("products/<int:product_id>/update/", product_update, name="product_update"),
    path("products/<int:product_id>/delete/", product_delete, name="product_delete"),
    path("orders/", get_orders, name="get_orders"),
    path("orders/create/", create_order, name="create_order"),
    path("orders/<int:order_id>/receive/", receive_order, name="receive_order"),
    path("orders/<int:order_id>/", get_order, name="get_order"),
    path("suppliers/", supplier_list, name="supplier_list"),
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/me/", MeView.as_view()),
]
