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
    console.log(quantity_product);
    console.log(quantity_selected);
    $(".alert-quantity").empty();
    if (quantity_product < quantity_selected) {
        $(".alert-quantity").append('Недостаточно товара! Снизьте количество товара!');
    }
    else {
        var add_in_basket = document.getElementById('add-in-basket');
        add_in_basket.click();
    };
};

function checkBasketQuantity() {
    var basket_quantity = Number(document.querySelector('.basket-quantity').firstChild.nodeValue);
    $(".basket-quantity").empty();
    $(".basket-quantity").append(basket_quantity+1);
};

function detailCheckBasket(id) {
    var select_quantity_product = Number(document.getElementById("quantity-product-"+id+"").firstChild.nodeValue);      // кол-во выбранного товара на складе
    var basket_quantity = Number(document.querySelector('.basket-quantity').firstChild.nodeValue);                      // текущее значение корзины
    var select_form = document.querySelector("#select-form-"+id+"");                                                    // находим форму с измененным товаром
    var select_quantity_form = Number(select_form.querySelector(".select-quantity").value);                             // находим значение измененного товара

    var col = 0;
    let select_quantity = document.querySelectorAll(".product-form");                                                   // находим все формы товаров на странице
    for (let el of select_quantity) {
        col = col + Number(el.querySelector('.select-quantity').value);
    };

    // находим измененную сумму цен товара
    var price_for_piece = Number(document.querySelector("#price-"+id+"").firstChild.nodeValue);
    var total_price_for_piece = price_for_piece * select_quantity_form

    // если выбранное количество меньше имеющегося то применить изменения
    if (select_quantity_form <= select_quantity_product) {
        $(".basket-quantity").empty();
        $(".basket-quantity").append(col);
        $("#total_price-"+id+"").empty();
        $("#total_price-"+id+"").append(total_price_for_piece);

        // находим и меняем общую сумму на все товары
        var col = 0;
        let products = document.querySelectorAll(".row"+".border-bottom"+".border-top"+".border-left"+".border-right"+".pb-3"+".pt-3"+".pl-3");
        for (let el of products) {
            col = col + Number(el.querySelector('.total_price').firstChild.nodeValue);
            console.log(col);
        };
        $("#get_total_price").empty();
        $("#get_total_price").append(col);
    };
};

function plusBtnInBasket(id) {
    var select_form = document.querySelector("#select-form-"+id+"")
    var select_quantity_form = select_form.querySelector(".select-quantity");
    var select_quantity_product = Number(document.getElementById("quantity-product-"+id+"").firstChild.nodeValue);      // кол-во товара

    var max = Number(select_quantity_form.value) + 1;
    if (max > select_quantity_product) {
        $("#alert-quantity-"+id+"").empty();
        $("#alert-quantity-"+id+"").append('Превышено количество товара');
    }
    else {
        select_quantity_form.value = max;
//        console.log(select_quantity_form.value);
    };
};

function minusBtnInBasket(id) {
    var select_form = document.querySelector("#select-form-"+id+"")
    var select_quantity_form = select_form.querySelector(".select-quantity");

    var min = Number(select_quantity_form.value) - 1;
    if (min > 0) {
        select_quantity_form.value = min;
    };
//    console.log(select_quantity_form.value);
};