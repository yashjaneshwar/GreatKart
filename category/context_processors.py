from .models import Category

""" takes request as an argument and return dictonary of category data as a context """
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
