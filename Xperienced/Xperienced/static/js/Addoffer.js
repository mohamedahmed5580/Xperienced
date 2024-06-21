$(document).ready(function() {
    $('#offer-form').submit(function() {
        event.preventDefault(); 
        if (validateForm()) {
            var formData = {
                'title': $('#title').val(),
                'description': $('#description').val(),
                'type': $('#type').val(),
                'category': $('#category').val(),
                'salary': $('#salary').val(),
                'status': $('#status').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // If using Django, get CSRF token
            };
            $.ajax({
                type: 'POST',
                url: 'sendoffers',  // Replace with your URL
                data: formData,
                success: function(response) {
                    console.log('Data sent successfully.');
                },
                error: function(error) {
                    console.log(error);
                }
            });
        } else {
            $('#alart').text('Please correct the errors in the form.').removeClass('d-n');
        }
    });
    
    function validateForm() {
        // Get form values
        const title = $('#title').val();
        const salary = $('#salary').val();
        const description = $('#description').val();
        const status = $('#status').val();
        
        // Get error message elements
        const titleError = $('#title-error');
        const salaryError = $('#salary-error');
        const descriptionError = $('#description-error');
        const statusError = $('#status-error');

        // Initialize validity flag
        let isValid = true;

        // Validate title
        if (title === '') {
            titleError.text('Title is required.').addClass('error-message');
            isValid = false;
        } else {
            titleError.text('').removeClass('error-message');
        }

        // Validate salary (must be a number and greater than 0)
        if (isNaN(salary) || salary <= 0) {
            salaryError.text('Please enter a valid salary.').addClass('error-message');
            isValid = false;
        } else {
            salaryError.text('').removeClass('error-message');
        }

        // Validate description length (must be at least 100 characters)
        if (description.length < 10 ||description.length > 200 || description === '') {
            descriptionError.text('Description is required, and must be at least 50 characters long and no more than 200 characters long.').addClass('error-message');
            isValid = false;
        } else {
            descriptionError.text('').removeClass('error-message');
        }

        // Validate status
        if (status === '') {
            statusError.text('Status is required.').addClass('error-message');
            isValid = false;
        } else {
            statusError.text('').removeClass('error-message');
        }

        return isValid;
    }
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
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

});