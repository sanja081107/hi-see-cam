from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .utils import DataMixin
from cart.forms import CartAddOneProductForm
from django.views.generic import DetailView, ListView, CreateView

from .models import *
from .forms import *
from cart.cart import Cart


def home(request):
    return render(request, 'main/index.html', context={'title': 'Главная страница'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def validate_order(request):        # При нажатии на оформить заказ идет проверка на пустую корзину
    if len(Cart(request)) == 0:
        return redirect('cart:cart_detail')
    else:
        return redirect('ordering')


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
        context['title'] = 'Подробнее о камере'
        context['block_title'] = 'Подробнее о камере'
        return context


class CameraListView(DataMixin, ListView):
    model = Cameras
    template_name = 'main/camera_list.html'
    context_object_name = 'cams'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Видеокамеры', block_title='Список видеокамер')
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


class OrderingView(CreateView):
    form_class = OrderForm
    template_name = 'main/ordering.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = AbstractUser
        cart = Cart(self.request)
        s = ''
        i = 0
        for el in cart:
            i += 1
            s += f'{i}) ' + str(el['product']) + f" {el['price']} p. " + str(el['quantity']) + 'шт. \n'
        form.instance.quantity = s
        form.instance.price = Cart(self.request).get_total_price()

        errors = 0
        cams = []
        for el in cart:
            count = 0
            cam = Cameras.objects.filter(id=el['product'].id, quantity__gt=0)
            if cam:
                count = cam[0].quantity
            if el['quantity'] <= count:
                cam[0].quantity -= el['quantity']
                cams.append(cam[0])
            else:
                errors += 1
        if errors == 0:
            for el in cams:
                el.save()
            cart.clear()
            return super().form_valid(form)
        else:
            return redirect('not_enough_product')


def not_enough_product(request):
    context = {
        'title': 'Ошибка заказа',
        'error': 'Пожалуйста, проверьте наличие товара!'
    }
    return render(request, 'main/errors.html', context)


# -----------------------------------htmx-------------------------------------


def checking_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
    if form.is_valid():
        return HttpResponse("""<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">Купить товар(ы)</button>""")


def check_form_username(request):
    if request.method == 'GET':
        u = request.GET.get('username')
    if u == '' or u is None:
        return HttpResponse("""<button type="submit" class="btn btn-primary">Купить товар(ы)</button>""")


def check_form_phone(request):
    if request.method == 'GET':
        p = request.GET.get('phone')
    if p == '' or p is None:
        return HttpResponse("""<button type="submit" class="btn btn-primary">Купить товар(ы)</button>""")


def check_form_email(request):
    if request.method == 'GET':
        e = request.GET.get('email')
    if e == '' or e is None:
        return HttpResponse("""<button type="submit" class="btn btn-primary">Купить товар(ы)</button>""")


def check_form_address(request):
    if request.method == 'GET':
        e = request.GET.get('address')
    if e == '' or e is None:
        return HttpResponse("""<button type="submit" class="btn btn-primary">Купить товар(ы)</button>""")


def check_form_note(request):
    if request.method == 'GET':
        e = request.GET.get('note')
    if e == '' or e is None:
        return HttpResponse("""<button type="submit" class="btn btn-primary">Купить товар(ы)</button>""")


def search(request):
    q = request.GET.get('q')
    if q is not None and q != '':
        results = Cameras.objects.filter(title__iregex=q)
    elif q == '':
        results = ''
    context = {'results': results}
    return render(request, 'main/search-results.html', context)


# -----------------------------------user-------------------------------------

class UserDetail(LoginRequiredMixin, DataMixin, DetailView):
    model = CustomUser
    slug_url_kwarg = 'slug'
    context_object_name = 'el'
    template_name = 'main/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пользователь', block_title='Мои данные')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class UserLogin(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/user_register.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserRegister(DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main/user_register.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        else:
            context = super().get_context_data()
            c_def = self.get_user_context(title='Вход', block_title='Регистрация')
            context = dict(list(context.items()) + list(c_def.items()))
            return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def user_logout(request):
    logout(request)             # стандартная ф-ия джанго для выхода пользователя
    return redirect('home')

