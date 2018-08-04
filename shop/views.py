from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.views import View
from .forms import LoginForm
from django.contrib.auth import login,authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
def product_list(request, category_slug=None):
    if request.user.is_authenticated:
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products})
    else:
        return HttpResponseRedirect(reverse('shop:loginview'))


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

class user_login(View):

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        emp = authenticate(username=username, password=password)
        if emp:
            login(request,emp)
        return HttpResponseRedirect(reverse('shop:product_list'))


    def get(self, request):
        return render(request, 'shop/login.html', {'form': LoginForm()})
