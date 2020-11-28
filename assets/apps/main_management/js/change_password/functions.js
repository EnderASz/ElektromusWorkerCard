function validateForm(){
    var password = document.new_password_form.new_password.value;
    var repeatedPassword = document.new_password_form.repeat_password.value;
    if(password && repeatedPassword){
        if(password == repeatedPassword){
            document.new_password_form.submit();
        } else {
            displayError("Podane hasła nie są identyczne!", "Proszę o ponowne wprowadzenie hasła, najlepiej do obu pól formularza.");
        }
    } else {
        displayError("Brak podanego hasła!", "Jedno lub więcej z pól formularza pozostało puste. Proszę o uzupełnienie ich identycznymi hasłami.");
    }
}

function displayError(errorHeaderMessage, errorDescriptionMessage){
    document.querySelector("#error-box > h5").innerHTML = errorHeaderMessage;
    document.querySelector("#error-box > p").innerHTML = errorDescriptionMessage;
    document.querySelector("#error-box").classList.toggle('invisible', false);
}