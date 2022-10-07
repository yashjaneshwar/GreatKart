from tkinter import E
from django.shortcuts import get_object_or_404, render

from category.models import Category
from .models import Product

# by default slug in None in url means not present


def store(request, category_slug=None):
	categories = None
	products = None

	# if there is something in slug like shirt, jacket
	# Ex: 'store/shirt' in url than only perform selective database operations
	if category_slug != None:
		# get_object_or_404(model name, model's slug field name = object name to store slug in url)
		categories = get_object_or_404(Category, slug=category_slug)
		products = Product.objects.filter(category=categories, is_available=True)
		product_count = products.count()

	else:
		# if its just 'store/' in url than fetch all details

		products = Product.objects.all().filter(is_available=True)
		product_count = products.count()

	context = {
		'products': products,
		'product_count': product_count,
	}

	return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
	# first we need to get category of product, category is present in store app model and slug is present is category app model
	# here we are accessing category of product as a slugfield type so we use category__slug
	try:
		single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
	except Exception as e:
		raise e 
	
	context = {
		'single_product': single_product,
	}
	return render(request, 'store/product_detail.html', context)