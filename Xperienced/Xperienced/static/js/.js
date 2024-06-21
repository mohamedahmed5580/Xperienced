$(document).ready(function() {
    console.log('in send requesrt.');
    $('#edit-profile-form').submit(function(event) {
        event.preventDefault();
        console.log('in edit-profile-form.');
        var formData = {
            'first_name': $('#firstname').val(),
            'last_name': $('#lastname').val(),
            'username': $('#username').val(),
            'email': $('#email').val(),
            'phone': $('#phone').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // Get CSRF token
        };
        console.log(formData);
        
        $.ajax({
            type: 'POST',
            url: 'edit',  // Replace with your Django URL
            data: formData,
            success: function(response) {
                console.log('Data send success.');
                location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#edit-about-form').submit(function(event) {
        event.preventDefault();
        console.log('in edit-description-form.');
        var formData = {
            'description': $('#description').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // Get CSRF token
        };
        console.log(formData);
        
        $.ajax({
            type: 'POST',
            url: 'editabout',
            data: formData,
            success: function(response) {
                console.log('Data send success.');
                location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#form-image').submit(function(event) {
        event.preventDefault();
        console.log('in edit-image-form.');
        console.log($('#image').val());
    
        var formData = new FormData(); // Create a new FormData object
    
        formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        
        let imageInput = $('#image')[0];
        let file = imageInput.files[0];
    
        if (file) {
            formData.append('image', file); // Appending the file correctly
        } else {
            alert("Please select an image");
            return; // Exit the function if no file is selected
        }
    
        $.ajax({
            type: 'POST',
            url: 'editimage', // Ensure the URL matches your Django URL pattern
            data: formData,
            processData: false, // Prevent jQuery from processing the data
            contentType: false, // Prevent jQuery from setting content type
            success: function(response) {
                console.log('Data send success.');
                location.reload(); // Reload the page to reflect the changes
            },
            error: function(error) {
                console.log(error);
            }
        });
    }); 
    
});
