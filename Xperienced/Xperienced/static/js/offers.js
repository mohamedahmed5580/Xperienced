$(document).ready(function() {
    console.log('in send requesrt.');
    $('#form-deloffer').submit(function(event) {
        event.preventDefault();
        console.log('in edit-profile-form.');
        var formData = {
            
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

    
});
