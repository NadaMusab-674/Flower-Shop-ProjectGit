from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.orders_view, name='orders'),
    path('products/', views.all_products_view, name='all_products'),
    path('contact/', views.contact_view, name='contact'),
    path('contact-messages/', views.contact_messages_view, name='contact_messages'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
]
