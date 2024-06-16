
$('#signup-form').submit(function(event) {
    event.preventDefault();
    var form=document.getElementById('signup-form');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var num='';
    var num2='';
    console.log($('#companyiO').val());
    console.log($('#myCheckbox').val());

    if ( $('#companyiO').val() == ''){
        num="False";
        num2='True'
    }else{
        num="True";
        num2="False";
    }

    if(validateForm()==true){
        $.ajax({
            type: 'POST',
            url: 'signup',
            headers: { "X-CSRFToken": csrftoken },
            data: {
                username: $('#username').val(),
                email: $('#email').val(),
                password1: $('#password').val(),
                password2: $('#confirm-password').val(),
                company_name: $('#companyiO').val(),
                is_admin: num,
                is_user: num2,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response) {
                console.log('Data sent successfully.');
                form.submit()
            },
            error: function(error) {
                console.log('An error occurred.');
                console.log(error);
            }
        });
    }else{
        console.log('Form is not valid');
    }

});

$('#login-form').submit(function(event) {
    var form=document.getElementById('login-form');
    var username = $('#username').val();
    var password = $('#password').val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    console.log( username)
    console.log( password)
    if (validateLoginForm) {
        $.ajax({
            type: 'POST',
            url: 'api/login',
            headers: { "X-CSRFToken": csrftoken },
            data: {
            username: $('#username').val(),
            password: $('#password').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'POST'
            },
            beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        success: function(response) {
            console.log('Data sent successfully.');
            
        },
        error: function(error) {
            console.log('An error occurred.');
            console.log(error);
        }
    
        });
    
    }else{
        console.log('Form is not valid');
    }


});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function validateForm() {
    const name = $('#username').val();
    const email = $('#email').val(); 
    const password = $('#password').val();
    const confirm_password = $('#confirm-password').val();
    const nameError = $('#name-error');
    const emailError = $('#email-error');
    const passwordError = $('#password-error');
    const confirm_passwordError = $('#confirm-password-error');

    nameError.text("");
    emailError.text("");
    passwordError.text("");
    confirm_passwordError.text("");

    let isValid = true;

    if (name === "" || /\d/.test(name)) {
        nameError.addClass('error-message');
        nameError.text("Please enter your name properly.");
        isValid = false;
    } else {
        nameError.removeClass('error-message');
    }

    if (email === "" || !email.includes("@")) {
        emailError.addClass('error-message');
        emailError.text("Please enter a valid email address.");
        isValid = false;
    } else {
        emailError.removeClass('error-message');
    }

    if (password === "" || password.length < 8) {
        passwordError.addClass('error-message');
        passwordError.text("Please enter a password with at least 8 characters.");
        isValid = false;
    } else {
        passwordError.removeClass('error-message');
    }

    if (confirm_password === "" || confirm_password.length < 8 || password !== confirm_password) {
        confirm_passwordError.addClass('error-message');
        confirm_passwordError.text("The passwords do not match.");
        isValid = false;
    } else {
        confirm_passwordError.removeClass('error-message');
    }

    const checkbox = document.getElementById('myCheckbox');

    if (checkbox.checked) {
        const companyError = $('#company-error');
        const company = $('#company').val();
        companyError.text("");

        if (company === "") {
            companyError.text("Please select your course.");
            isValid = false;
        }
    }

    return isValid;
}

function validateLoginForm(){
    const name = $('#username').val();
    const password = $('#password').val();
    const nameError = $('#name-error');
    const passwordError = $('#password-error');

    if (name === "" || /\d/.test(name)) {
        nameError.addClass('error-message');
        nameError.text("the UserName is not correct.");
        isValid = false;
    } else {
        nameError.removeClass('error-message');
    }

    if (password === "" || password.length < 8) {
        passwordError.addClass('error-message');
        passwordError.text("the Password is not correct.");
        isValid = false;
    } else {
        passwordError.removeClass('error-message');
    }

    return isValid;
    
}