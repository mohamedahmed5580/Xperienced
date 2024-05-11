const form = document.getElementById('form');

document.getElementById('form').addEventListener('submit', function(event) {
  event.preventDefault();
  const formData = new FormData(form);
  fetch('/api/login/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(Object.fromEntries(formData)),
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })

});
