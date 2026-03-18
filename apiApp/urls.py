from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<slug:slug>/', views.product_detail, name='product-detail'),
    path('categories/', views.category_list, name='category-list'),
    path('categories/<slug:slug>/', views.category_detail, name='category-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('update-cartitem-quantity/', views.update_cartitem, name='update-cartitem'),
    path('add-review/', views.add_review, name='add-review'),
    path('update-review/<int:pk>/', views.update_review, name='update-review'),
    path('delete-review/<int:pk>/', views.delete_review, name='delete-review'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),

]
