from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .utils import DataMixin
from cart.forms import CartAddProductForm, CartAddOneProductForm
from django.views.generic import DetailView, TemplateView, ListView, CreateView

from .models import *
from .forms import *
from cart.cart import Cart


def home(request):
    return render(request, 'main/index.html')


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


def validate_order(request):        # При нажатии на оформить заказ идет проверка на пустую корзину
    if len(Cart(request)) == 0:
        return redirect('cart:cart_detail')
    else:
        return redirect('ordering')


def checking_order(request):
    form = OrderForm(request.POST)
    if form.is_valid():
        return HttpResponse("""<button id="check-ordering" type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">Купить товар(ы)</button>""")


class OrderingView(CreateView):
    form_class = OrderForm
    template_name = 'main/ordering.html'

    def get_success_url(self):
        return reverse_lazy('home')


class CameraDetailView(DetailView):
    model = Cameras
    template_name = 'main/camera_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'el'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cart_one_product_form'] = CartAddOneProductForm()
        cart = Cart(self.request)
        lst = []
        for el in cart:
            lst.append(el['product'])
        context['products'] = lst
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
        cart = Cart(self.request)
        lst = []
        for el in cart:
            lst.append(el['product'])
        context['products'] = lst
        return context

    def get_queryset(self):
        return Cameras.objects.filter(quantity__gt=0)
