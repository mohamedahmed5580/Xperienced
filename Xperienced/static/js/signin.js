$(document).ready(function() {
    $('#signup-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the default way
        
        if (validateForm()) {
             // Collect form data
             var formData = {
                'first_name': $('#firstname').val(),
                'last_name': $('#lastname').val(),
                'username': $('#username').val(),
                'email': $('#email').val(),
                'phone': $('#phone').val(),
                'password': $('#password').val(),
                'confirm_password': $('#confirm-password').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // Get CSRF token
            };
            $.ajax({
                type: 'POST',
                url: 'signup', // Change this to your actual signup URL
                data: formData,
                success: function(response) {
                    console.log('Data sent successfully.');
                },
                error: function(error) {
                    console.log('An error occurred.');
                    console.log(error);
                }
            });   
        }
      
    });
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
    const firstName = document.getElementById('firstname').value.trim();
    const lastName = document.getElementById('lastname').value.trim();
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirm-password').value.trim();

    const nameError = document.getElementById('name-error');
    const usernameError = document.getElementById('username-error');
    const emailError = document.getElementById('email-error');
    const phoneError = document.getElementById('phone-error');
    const passwordError = document.getElementById('password-error');
    const confirmPasswordError = document.getElementById('confirm-password-error');

    nameError.textContent = '';
    usernameError.textContent = '';
    emailError.textContent = '';
    phoneError.textContent = '';
    passwordError.textContent = '';
    confirmPasswordError.textContent = '';

    let isValid = true;

    if (firstName === "" || /\d/.test(firstName)) {
        nameError.textContent = "Please enter your first name properly.";
        isValid = false;
    }

    if (lastName === "" || /\d/.test(lastName)) {
        nameError.textContent = "Please enter your last name properly.";
        isValid = false;
    }

    if (username === "") {
        usernameError.textContent = "Username is required.";
        isValid = false;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        emailError.textContent = "Please enter a valid email address.";
        isValid = false;
    }

    const phonePattern = /^[0-9]{10,15}$/;
    if (!phonePattern.test(phone)) {
        phoneError.textContent = "Invalid phone number.";
        isValid = false;
    }

    if (password === "" || password.length < 8) {
        passwordError.textContent = "Please enter a password with at least 8 characters.";
        isValid = false;
    }

    if (confirmPassword === "" || confirmPassword.length < 8 || password !== confirmPassword) {
        confirmPasswordError.textContent = "The passwords do not match.";
        isValid = false;
    }

    return isValid;
}