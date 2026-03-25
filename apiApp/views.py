import stripe
from django.conf import settings
from django.shortcuts import render
#from huggingface_hub import User
from rest_framework.decorators import api_view
from .models import Cart, CartItem, Category, CustomUser, OrderItem, Orders, Product, Review, Wishlist
from .serializers import ProductSerializer,ProductDetailSerializer, CategoryListSerializer, CategoryDetailSerializer,CartSerializer, CartItemSerializer, CartStatusSerializer, ReviewSerializer, WishlistSerializer
from rest_framework.response import Response
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.WEBHOOK_SECRET


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


@api_view(['DELETE'])
def delete_cartItem(request,pk):
    cartitem= CartItem.objects.get(id=pk)
    cartitem.delete()
    return Response({"message": "Cart item deleted successfully", "status": 204})



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

@api_view(['GET'])
def search_products(request):
    query = request.query_params.get('query', '')
    if not query:
        return Response({"No search query provided"}, status=400)
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)|
    Q(category__name__icontains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



    #! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
@api_view(['POST'])
def create_checkout_session(request):
    cart_code = request.data.get('cart_code')
    email = request.data.get('email')

    cart = Cart.objects.get(card_code=cart_code)

    try:
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            }
            for item in cart.cart_items.all()  # অথবা cart.cart_items.all()
        ]

        checkout_session = stripe.checkout.Session.create(
            customer_email=email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
            metadata={'cart_code': cart_code}
        )

        return Response({
            'id': checkout_session.id,
            'url': checkout_session.url
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)
    





# Using Django


# Use the secret provided by Stripe CLI for local testing
# or your webhook endpoint's secret.


@csrf_exempt
def my_webhook_view(request):
  print("🔥 Webhook called")
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
    print("✅ Event:", event['type'])

    if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            cart_code = session.get('metadata', {}).get('cart_code')

            print("🛒 Cart Code:", cart_code)

            fulfill_checkout(session, cart_code)
  except ValueError as e:
    # Invalid payload
    print("❌ Error:", str(e))
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    print("❌ Error:", str(e))
    return HttpResponse(status=400)

  if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
  ):
    session = event['data']['object']
    cart_code = session.get('metadata', {}).get('cart_code')
    fulfill_checkout(session, cart_code)



  return HttpResponse(status=200)


def fulfill_checkout(sessioon, cart_code):
    order = Orders.objects.create(
        stripe_checkout_id=sessioon['id'],
        amount=sessioon['amount_total'] / 100,
        currency=sessioon['currency'],
        customer_email=sessioon['customer_email'],
        status='paid',)
    
    cart = Cart.objects.get(card_code=cart_code)
    cartitems = cart.cart_items.all()

    for item in cartitems:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
            
        )
    cart.cart_items.all().delete()