const form = document.getElementById('form');

document.getElementById('form').addEventListener('submit', function(event) {
  event.preventDefault();

  fetch('/api/login/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          firstname: document.getElementById('firstname').value,
          lastname: document.getElementById('lastname').value,
          username: document.getElementById('username').value,
          email: document.getElementById('email').value,
          phone: document.getElementById('phone').value,
          password: document.getElementById('Password').value,
          confirm_password: document.getElementById('ConfirmPassword').value
      }),
  })
  .then(response => response.json())
  .then(data => {
      console.log(data); 
      
  })

});
