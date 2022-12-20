function CheckForm() {

    var name = document.getElementById("name");
    var surname = document.getElementById("surname");
    var errors = document.getElementById("errors");
    $("#errors").empty();

    if (name.value == '' && surname.value == '') {
        $("#errors").append('<br>введите имя и фамилию')
    }
    else {
        if (name.value == '') {
            $("#errors").append('<br>введите имя');
        };
        if (surname.value == '') {
            $("#errors").append('<br>введите фамилию');
        };
    };
    if (name.value != '' && surname.value != '') {
        document.getElementById("formIsOk").click();
    };
//    if (name.value != '' && surname.value != '') {
//        $("#order-form").append("<br><input placeholder='your email' id='email' name='email' type='email'><br>");
//        name.hidden;
//        surname.hidden;
//    };
};

function checkAddInBasket() {
    var quantity_product = Number(document.getElementById('quantity-product').firstChild.nodeValue);     // достаем данные из тега (количество доступного товара)
    var quantity_selected = Number(document.getElementById('id_quantity').value);                        // достаем данные из тега (количество выбранного товара)
//    console.log(quantity_product);
//    console.log(quantity_selected);
    $("#alert-quantity").empty();
    if (quantity_product < quantity_selected) {
        $("#alert-quantity").append('Недостаточно товара! Снизьте количество товара!');
    }
    else {
        var add_in_basket = document.getElementById('add-in-basket');
        add_in_basket.click();
    };
};

function checkBasketQuantity() {
    var basket_quantity = Number(document.getElementById('basket-quantity').firstChild.nodeValue);
    $("#basket-quantity").empty();
    $("#basket-quantity").append(basket_quantity+1);
};