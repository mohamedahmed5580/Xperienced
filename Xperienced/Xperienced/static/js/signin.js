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
                window.location.href = "/";

            },
            error: function(error) {
                console.log('An error occurred.');
                console.log(error);
            }
        });
    }
  
});

// Function to get CSRF cookie value
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

// Function to check if HTTP method is safe for CSRF
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Function to validate form fields
function validateForm() {
    const firstName = $('#firstname').val();
    const lastName = $('#lastname').val();
    const email = $('#email').val(); 
    const password = $('#password').val();
    const confirmPassword = $('#confirm-password').val();
    const username = $('#username').val();
    const phone = $('#phone').val();

    let isValid = true;

    // Clear previous error messages
    $('.error-message').text('').removeClass('error-message');

    // Validation checks
    if (firstName === "" || /\d/.test(firstName)) {
        $('#name-error').text("Please enter your first name properly.").addClass('error-message');
        isValid = false;
    }

    if (lastName === "" || /\d/.test(lastName)) {
        $('#name-error').text("Please enter your last name properly.").addClass('error-message');
        isValid = false;
    }

    if (username === "") {
        $('#username-error').text("Username is required.").addClass('error-message');
        isValid = false;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        $('#email-error').text("Please enter a valid email address.").addClass('error-message');
        isValid = false;
    }

    const phonePattern = /^[0-9]{10,15}$/;
    if (!phonePattern.test(phone)) {
        $('#phone-error').text("Invalid phone number.").addClass('error-message');
        isValid = false;
    }

    if (password === "" || password.length < 8) {
        $('#password-error').text("Please enter a password with at least 8 characters.").addClass('error-message');
        isValid = false;
    }

    if (confirmPassword === "" || confirmPassword.length < 8 || password !== confirmPassword) {
        $('#confirm-password-error').text("The passwords do not match.").addClass('error-message');
        isValid = false;
    }

    return isValid;
}
