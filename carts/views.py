from django.shortcuts import redirect, render

from carts.models import CartItem
from store.models import Product
from .models import Cart,CartItem

from django.http import HttpResponse 


def _cart_id(request):
	# fetch session_key from request and create session_key if it is null
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart


def add_cart(request, product_id):
	# get the product
	product = Product.objects.get(id = product_id)  
	try:
		""" 
		# get the cart using cart_id present in the session based on current request,
		# so that it will match cart_id with session_id

		"""
		cart = Cart.objects.get(cart_id = _cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(cart_id = _cart_id(request))
		cart.save()

	try:
		# to put fetched product inside cart,eventuall all fetched products will become cart_item
		# here combining product and cart to make cart_item
		cart_item = CartItem.objects.get(product = product, cart = cart)
		cart_item.quantity += 1
		cart_item.save()

	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(
			product = product,
			cart = cart,
			quantity = 1,
		)
		cart_item.save()

	return HttpResponse(cart_item.quantity)
	exit()
	return redirect('cart')

def cart(request, total=0, quantity=0, cart_items = None):
	""" to render cart item and its content """
	try:
		cart = Cart.objects.get(cart_id=cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, is_active = True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			quantity += cart_item.quantity
	
	except ObjectNotExist:
		pass 	# just ignore

	context ={
		'total': total,
		'quantity': quantity,
		'cart_items': cart_items,
	}
	return render(request, 'store/cart.html', context)