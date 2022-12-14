from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .utils import DataMixin
from cart.forms import CartAddProductForm
from django.views.generic import DetailView, TemplateView, ListView

from .models import *


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
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        print(name, surname)
    return render(request, 'main/index.html')


class OrderingView(TemplateView):
    template_name = 'main/ordering.html'


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
        return context
