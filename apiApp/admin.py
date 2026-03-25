from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, OrderItem, Orders, Product, Cart, CartItem, Review, ProductRating, Wishlist


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'featured')

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Category, CategoryAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('card_code', 'created_at', 'updated_at')

admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

admin.site.register(CartItem, CartItemAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')

admin.site.register(Review, ReviewAdmin)


class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'average_rating', 'total_reviews')

admin.site.register(ProductRating, ProductRatingAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created')
admin.site.register(Wishlist, WishlistAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('stripe_checkout_id', 'customer_email', 'amount', 'currency', 'status', 'created_at')
admin.site.register(Orders, OrdersAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
admin.site.register(OrderItem, OrderItemAdmin)