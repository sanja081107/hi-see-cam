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
        }
        if (surname.value == '') {
            $("#errors").append('<br>введите фамилию');
        };
    };
    if (name.value != '' && surname.value != '') {
        document.getElementById("formIsOk").click();
    };

};