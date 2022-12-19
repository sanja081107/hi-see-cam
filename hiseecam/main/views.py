from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .utils import DataMixin
from cart.forms import CartAddProductForm, CartAddOneProductForm
from django.views.generic import DetailView, TemplateView, ListView

from .models import *
from .forms import *
from cart.cart import Cart


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def search(request):
    q = request.GET.get('q')
    if q is not None and q != '':
        results = Cameras.objects.filter(title__iregex=q)
    elif q == '':
        results = ''
    context = {'results': results}
    return render(request, 'main/search-results.html', context)


def home(request):
    return render(request, 'main/index.html')


def validate_order(request):
    if len(Cart(request)) == 0:
        return redirect('cart:cart_detail')
    else:
        return redirect('ordering')


def add_order(request):
    cart = Cart(request)
    for el in cart:
        print(el)

    return redirect('home')


class OrderingView(TemplateView):
    template_name = 'main/ordering.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['order_product_form'] = OrderProductsForm()
        context['order_form'] = OrderForm()
        return context

class CameraDetailView(DetailView):
    model = Cameras
    template_name = 'main/camera_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'el'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cart_product_form'] = CartAddProductForm()
        return context


class CameraListView(DataMixin, ListView):
    model = Cameras
    template_name = 'main/camera_list.html'
    context_object_name = 'cams'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Список видеокамер')
        context = dict(list(context.items()) + list(c_def.items()))
        context['cart_one_product_form'] = CartAddOneProductForm()
        return context
