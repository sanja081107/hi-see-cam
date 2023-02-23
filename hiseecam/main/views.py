from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Max
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from random import randint as rand

from .utils import DataMixin
from cart.forms import CartAddOneProductForm
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView

from .models import *
from .forms import *
from cart.cart import Cart


def home(request):
    max_pk = Cameras.objects.all().aggregate(max_pk=Max("pk"))['max_pk']
    n = []
    while True:
        x = rand(1, max_pk)
        if x not in n:
            n.append(x)
        if len(n) == 3:
            break
    cams = Cameras.objects.filter(pk__in=n)
    context = {
        'title': 'Главная страница',
        'block_title': 'Главная страница',
        'cams': cams
    }
    return render(request, 'main/index.html', context)


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
        c_def = self.get_user_context(title='Видеокамеры', block_title='Каталог видеокамер')
        context = dict(list(context.items()) + list(c_def.items()))
        context['cart_one_product_form'] = CartAddOneProductForm()
        cart = Cart(self.request)

        lst = []
        for el in cart:
            lst.append(el['product'])
        context['products'] = lst

        max_price = self.request.GET.get('max_price')
        min_price = self.request.GET.get('min_price')

        if max_price is None and min_price is None:
            context['FilterCameraForm'] = FilterCameraForm()
        else:
            context['FilterCameraForm'] = FilterCameraForm(self.request.GET)

        context['filter_camera'] = self.request.GET.get('filter_camera')
        context['min_price'] = self.request.GET.get('min_price')
        context['max_price'] = self.request.GET.get('max_price')

        return context

    def get_queryset(self):
        filter_cams = self.request.GET.get('filter_camera')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if max_price == '0' or max_price == 'None' or max_price == '' or max_price is None:
            max_price = 9999999
        if min_price == '0' or min_price == 'None' or min_price == '' or min_price is None:
            min_price = 0

        if filter_cams:
            if filter_cams == 'none':
                return Cameras.objects.filter(quantity__gt=0, price__gt=min_price, price__lt=max_price)
            elif filter_cams == 'price_up':
                return Cameras.objects.filter(quantity__gt=0, price__gt=min_price, price__lt=max_price).order_by('price')
            elif filter_cams == 'price_down':
                return Cameras.objects.filter(quantity__gt=0, price__gt=min_price, price__lt=max_price).order_by('-price')
            elif filter_cams == 'popular':
                return Cameras.objects.filter(quantity__gt=0, price__gt=min_price, price__lt=max_price).order_by('-sold_count')
            else:
                return Cameras.objects.filter(quantity__gt=0, price__gt=min_price, price__lt=max_price)
        else:
            return Cameras.objects.filter(quantity__gt=0, price__gt=min_price, price__lt=max_price)


def filter_check(request):
    filter_cams = request.GET.get('filter_camera')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if max_price == '0' or max_price == 'None' or max_price == '' or max_price is None:
        max_price_new = 9999999
    else:
        max_price_new = max_price
    if min_price == '0' or min_price == 'None' or min_price == '' or min_price is None:
        min_price_new = 0
    else:
        min_price_new = min_price

    if filter_cams:
        if filter_cams == 'none':
            cams = Cameras.objects.filter(quantity__gt=0, price__gt=min_price_new, price__lt=max_price_new)
        elif filter_cams == 'price_up':
            cams = Cameras.objects.filter(quantity__gt=0, price__gt=min_price_new, price__lt=max_price_new).order_by('price')
        elif filter_cams == 'price_down':
            cams = Cameras.objects.filter(quantity__gt=0, price__gt=min_price_new, price__lt=max_price_new).order_by('-price')
        elif filter_cams == 'popular':
            cams = Cameras.objects.filter(quantity__gt=0, price__gt=min_price_new, price__lt=max_price_new).order_by('-sold_count')
        else:
            cams = Cameras.objects.filter(quantity__gt=0, price__gt=min_price_new, price__lt=max_price_new)
    else:
        cams = Cameras.objects.filter(quantity__gt=0, price__gt=min_price_new, price__lt=max_price_new)

    if not cams:
        return HttpResponse('Нет результатов. Измените фильтр')
    else:
        paginator = Paginator(cams, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        cart = Cart(request)
        lst = []
        for el in cart:
            lst.append(el['product'])

        context = {
            'products': lst,
            'cams': page_obj,
            'cart_one_product_form': CartAddOneProductForm(),
            'paginator': paginator,
            'page_obj': page_obj,
            'min_price': min_price,
            'max_price': max_price,
            'filter_camera': filter_cams
            }
        return render(request, 'main/filter_result.html', context)


class OrderingView(DataMixin, CreateView):
    form_class = OrderForm
    template_name = 'main/ordering.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оформление заказа', block_title='Оформление заказа')
        if self.request.user.is_authenticated:
            user = self.request.user
            context['form'] = OrderForm(initial={'address': user.address, 'username': user.first_name, 'phone': user.mobile, 'email': user.email})

        cart = Cart(self.request)
        s = ''
        i = 0
        for el in cart:
            i += 1
            s += f'{i}) ' + str(el['product']) + f" - {el['price']}p. " + str(el['quantity']) + 'шт. \n'
        context['alert_cams'] = s
        context['alert_price'] = cart.get_total_price()
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.user = None

        cart = Cart(self.request)
        s = ''
        i = 0
        for el in cart:
            i += 1
            s += f'{i}) ' + str(el['product']) + f" {el['price']} p. " + str(el['quantity']) + 'шт. \n'
        price = cart.get_total_price()
        form.instance.quantity = s
        form.instance.price = price

        errors = 0
        cams = []
        for el in cart:
            count = 0
            cam = Cameras.objects.filter(id=el['product'].id, quantity__gt=0)
            if cam:
                count = cam[0].quantity
            if (el['quantity'] <= count) and (count != 0):
                cam[0].quantity -= el['quantity']
                cam[0].sold_count += el['quantity']
                cams.append(cam[0])
            else:
                errors += 1
        if errors == 0:
            for el in cams:
                el.save()
            cart.clear()

            subject = 'Оформление заказа'
            message = s + f'Закакз на общую сумму: {price}р. выполнен!'
            mail = self.request.POST['email']
            send_mail(subject, message, 'sanja081107@gmail.com', [mail])
            send_mail(subject, 'Поступил новый заказ', 'sanja081107@gmail.com', ['alexander_misyuta@mail.ru'])

            return super().form_valid(form)
        else:
            return redirect('not_enough_product')


def not_enough_product(request):
    context = {
        'title': 'Ошибка заказа',
        'error': 'Пожалуйста, проверьте наличие товара!'
    }
    return render(request, 'main/errors.html', context)


class FeedbackView(DataMixin, CreateView, ListView):
    template_name = 'main/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback')

    queryset = Feedback.objects.all()
    context_object_name = 'comments'
    paginate_by = 5

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            post = form.save()
            for item in self.request.FILES.getlist('images'):
                FeedbackPhotos.objects.create(images=item, post=post)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['image_form'] = FeedbackPhotosForm()
        c_def = self.get_user_context(title='Отзывы', block_title='Отзывы')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class GalleryView(TemplateView):
    template_name = 'main/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        posts = Gallery.objects.all()
        context['title'] = 'Галерея'
        context['block_title'] = 'Фото галерея'
        context['posts'] = posts
        return context


class GalleryDetailView(DetailView):
    model = Gallery
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    template_name = 'main/gallery_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        el = Gallery.objects.get(slug=self.kwargs['slug'])
        context['title'] = f"{el.title}"
        context['block_title'] = f"Фото работ"
        return context


class MyShoppingView(LoginRequiredMixin, ListView):
    template_name = 'main/my_shopping.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Order.objects.filter(user=self.request.user)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Мои покупки'
        context['block_title'] = 'Мои покупки'
        return context


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Контакты'
        context['block_title'] = 'Контакты'
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'О компании'
        context['block_title'] = 'О компании'
        return context


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
        print(p)
    if p == '' or p == '%2B375%20(xx)%20xxx-xx-xx' or p is None:
        print('yes')
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


class UserDetail(LoginRequiredMixin, DataMixin, DetailView, UpdateView):
    model = CustomUser
    slug_url_kwarg = 'slug'
    context_object_name = 'el'
    template_name = 'main/user_detail.html'

    form_class = CustomUserChangePhotoForm

    login_url = reverse_lazy('user_login')

    def get_success_url(self):
        user = CustomUser.objects.get(slug=self.kwargs['slug'])
        return user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пользователь', block_title='Мои данные')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class UserUpdate(LoginRequiredMixin, DataMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeFormWithoutPassword
    template_name = 'main/user_register.html'
    login_url = reverse_lazy('user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение данных', block_title='Изменение данных')
        context = dict(list(context.items()) + list(c_def.items()))

        if self.request.user.slug == self.kwargs['slug']:
            return context
        else:
            context['error'] = 'Ошибка доступа'
            return context

    def get_success_url(self):
        user = CustomUser.objects.get(slug=self.kwargs['slug'])
        return user.get_absolute_url()


class UserLogin(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/user_login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(title='Авторизация', block_title='Авторизация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def user_logout(request):
    logout(request)             # стандартная ф-ия джанго для выхода пользователя
    return redirect('home')


class UserRegister(DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main/user_register.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(title='Регистрация', block_title='Регистрация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class ChangePassword(DataMixin, PasswordChangeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(block_title='Изменение пароля')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class PasswordChangeDone(DataMixin, PasswordChangeDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(block_title='Пароль изменен успешно')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class PasswordReset(DataMixin, PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(block_title='Восстановление пароля')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class PasswordResetDone(DataMixin, PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(block_title='Восстановление пароля')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class PasswordResetConfirm(DataMixin, PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(block_title='Сброс пароля')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class PasswordResetComplete(DataMixin, PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(block_title='Сброс пароля выполнен')
        context = dict(list(context.items()) + list(c_def.items()))
        return context
