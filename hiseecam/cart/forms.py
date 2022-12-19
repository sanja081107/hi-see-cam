from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):           # вызываем форму на странице подробнее о товаре

    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                label='Количество',
                                widget=forms.Select(attrs={'class': 'form-control select-quantity'}))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CartAddOneProductForm(forms.Form):        # вызываем форму для каждого товара на странице со всех товарами

    quantity = forms.CharField(widget=forms.TextInput(attrs={'value': f'1', 'type': 'hidden'}))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
