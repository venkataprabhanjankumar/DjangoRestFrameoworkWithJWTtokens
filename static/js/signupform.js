function check(elem) {
    var password = document.getElementById('password');
    var flag = 1;
    if (elem.value.length > 0) {
        if (elem.value != password.value) {
            document.getElementById('alert').innerText = "confirm password does not match";

        } else {
            document.getElementById('alert').innerText = "";

        }
    } else {
        document.getElementById('alert').innerText = "please enter confirm password";

    }


}