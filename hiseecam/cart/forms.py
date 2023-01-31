from django import forms
from django.utils.safestring import mark_safe

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddForm(forms.Form):              # вызываем форму для каждого товара в корзине

    quantity = forms.CharField(label='Количество', widget=forms.TextInput(attrs={'class': 'form-control select-quantity', 'type': 'number', 'readonly': True}))

    update = forms.BooleanField(required=False,
                                initial=True,
                                widget=forms.HiddenInput)


class CartAddOneProductForm(forms.Form):    # вызываем форму для каждого товара на странице со всех товарами и на странице о товаре

    quantity = forms.CharField(widget=forms.TextInput(attrs={'value': f'1', 'type': 'hidden'}))

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CartAddProductForm(forms.Form):       # не используем

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,
                                      label='Количество',
                                      widget=forms.Select(attrs={'class': 'form-control select-quantity'}))

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
