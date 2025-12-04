from django.urls import path
from core.views.product_view import product_list, product_create, product_update, product_delete
from core.views.order_view import create_order, get_orders


urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:product_id>/update/', product_update, name='product_update'),
    path('products/<int:product_id>/delete/', product_delete, name='product_delete'),

    path("orders/", get_orders, name="get_orders"),
    path("orders/create", create_order, name="create_order"),
]



