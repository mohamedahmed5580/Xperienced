$(document).ready(function() {
    $('#signup-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the default way
        
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
            url: 'signup/', // Add the trailing slash here
            data: formData,
            success: function(response) {
                console.log('Data sent successfully.');
            },
            error: function(error) {
                console.log('An error occurred.');
                console.log(error);
            }
        });
    });

});