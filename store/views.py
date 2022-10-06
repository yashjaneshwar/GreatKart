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
