from django.shortcuts import render
#from huggingface_hub import User
from rest_framework.decorators import api_view
from .models import Cart, CartItem, Category, CustomUser, Product, Review, Wishlist
from .serializers import ProductSerializer,ProductDetailSerializer, CategoryListSerializer, CategoryDetailSerializer,CartSerializer, CartItemSerializer, CartStatusSerializer, ReviewSerializer, WishlistSerializer
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, slug):
   product = Product.objects.get(slug=slug)
   serializer = ProductDetailSerializer(product)  
   return Response(serializer.data)


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')

    cart, created = Cart.objects.get_or_create(card_code=cart_code)
    product = Product.objects.get(id=product_id)

    cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cartitem.quantity += 1
    cartitem.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['PUT'])
def update_cartitem(request):
    cartitem_id = request.data.get('item_id')
    quantity =int( request.data.get('quantity'))

    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()

    serializer = CartItemSerializer(cartitem)
    return Response({"data": serializer.data , "message": "Cart item updated successfully"})


@api_view(['POST'])
def add_review(request):

    product_id = request.data.get('product_id')
    email = request.data.get('email')
    rating = request.data.get('rating')
    # rwview_text = request.data.get('review')
    comment = request.data.get('review')

    product = Product.objects.get(id=product_id)
    user = CustomUser.objects.get(email=email)

    if Review.objects.filter(product=product, user=user).exists():
        return Response({"message": "You have already reviewed this product."}, status=400)

    review = Review.objects.create(product=product, user=user,rating=rating, comment=comment)

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['PUT'])
def update_review(request, pk):
    from django.shortcuts import get_object_or_404

    review = get_object_or_404(Review, id=pk)

    rating = request.data.get('rating')
    review_text = request.data.get('comment')

    review.rating = rating
    review.comment = review_text
    review.save()

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_review(request,pk):
    review= Review.objects.get(id=pk)
    review.delete()
    return Response({"message": "Review deleted successfully", "status": 204})



from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404

@api_view(['POST'])
def add_to_wishlist(request):
    product_id = request.data.get('product_id')
    email = request.data.get('email')

    product = get_object_or_404(Product, id=product_id)
    user = get_object_or_404(CustomUser, email=email)

    existing = Wishlist.objects.filter(product=product, user=user)

    if existing.exists():
        existing.delete()
        return Response({"message": "Wishlist removed"}, status=200)

    new_wishlist = Wishlist.objects.create(product=product, user=user)

    serializer = WishlistSerializer(new_wishlist)
    return Response(serializer.data, status=201)