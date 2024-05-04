$(document).ready(function() {
    $("#btn-primary").click(function(event) {
      event.preventDefault();
  
      var isValid = true;
  
      // Validate first name
      if ($("#first-name").val() == "") {
        $("#first-name").addClass("error");
        isValid = false;
      } else {
        $("#first-name").removeClass("error");
      }
  
      // Validate last name
      if ($("#last-name").val() == "") {
        $("#last-name").addClass("error");
        isValid = false;
      } else {
        $("#last-name").removeClass("error");
      }
  
      // Validate email
      if ($("#email").val() == "") {
        $("#email").addClass("error");
        isValid = false;
      } else {
        $("#email").removeClass("error");
      }
  
      // Validate phone number
      if ($("#phone").val() == "") {
        $("#phone").addClass("error");
        isValid = false;
      } else {
        $("#phone").removeClass("error");
      }
  
      // Validate password
      if ($("#password").val() == "") {
        $("#password").addClass("error");
        isValid = false;
      } else {
        $("#password").removeClass("error");
      }
  
      // Validate confirm password
      if ($("#confirm-password").val() == "") {
        $("#confirm-password").addClass("error");
        isValid = false;
      } else {
        $("#confirm-password").removeClass("error");
      }
  
      // If all fields are valid, submit the form
      if (isValid) {
        $("#signup-form").submit();
      }
    });
  });