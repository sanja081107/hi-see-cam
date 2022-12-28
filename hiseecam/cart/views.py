from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from main.models import Cameras
from .cart import Cart
from .forms import CartAddProductForm, CartAddForm


@require_POST
def cart_add_one_camera_detail(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Cameras, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return HttpResponse('В корзине <i class="fa-solid fa-check"></i>')


@require_POST
def cart_add_one_camera_list(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Cameras, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    # return redirect('camera_list')
    return HttpResponse('<i class="fa-solid fa-check card-body-form"></i>')


@require_POST
def check_add_in_basket(request, product_id):
    product = get_object_or_404(Cameras, id=product_id)
    quantity = request.POST['quantity']
    col_product = product.quantity
    if int(quantity) > col_product:
        return HttpResponse('Недостаточно товара! Снизьте количество товара!')
    else:
        cart = Cart(request)
        product = get_object_or_404(Cameras, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        return HttpResponse()


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Cameras, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


def clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('home')


def print_cart(request):
    cart = Cart(request)
    for item in cart:
        print(item)
    print(cart.get_total_price())
    return redirect('home')
