
var offerDataArray = JSON.parse(localStorage.getItem('offerDataArray')) || [];
var btn=document.getElementById("btnAdd");
var alart_error= document.getElementById('alart');
btn.onclick = function() {
    var title = document.getElementById("title").value;
    var salary = document.getElementById("salary").value;
    var skills = document.getElementById("skills").value;
    var type = document.getElementById("type").value;
    var description = document.getElementById("description").value;
    var category = document.getElementById("category").value;
    if (title == '' || salary ==''  || skills ==''  || description ==''  || type ==''  || category=='') {
        alart_error.classList.remove('d-n');
        alart_error.classList.add('d-b');
        alart_error.textContent="you have empty field";
        return false;
      }else{
          var offerData = {
              title: title,
              salary: salary,
              skills: skills,
              type: type,
              description: description,
              category: category,
          };
          offerDataArray.push(offerData);
          window.localStorage.setItem('offerDataArray', JSON.stringify(offerDataArray));
          alart_error.classList.remove('d-b');
          alart_error.classList.add('d-n');
      }
}

document.addEventListener("DOMContentLoaded", () => {
    let requestForm = document.getElementById("new-request-form");
    requestForm.onsubmit = addRequest;
})

  
function updateJSONFile() {
    var jsonData = JSON.stringify(offerDataArray);
    var blob = new Blob([jsonData], { type: 'application/json' });
    var url = URL.createObjectURL(blob);

    var a = document.createElement('a');
    a.href = url;
    a.download = 'offer_data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}



function HelpRequest(title, description, skills, category, budget) {
    this.title = title;
    this.description = description;
    this.skills = skills;
    this.category = category;
    this.budget = budget;
}

function addRequest() {
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;
    let skills = document.getElementById("skills").value;
    let category = document.getElementById("category").value;
    let budget = document.getElementById("salary").value;

    let request = new HelpRequest(title, description, skills, category, budget);
    fetch('find/submit', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            request: request
        }),
    }).then(response => response.json()).then(console.log(response));
    let requests = JSON.parse(localStorage.getItem('offerDataArray')) || [];
    requests.push(request);
    window.localStorage.setItem('offerDataArray', JSON.stringify(requests));
    return false;
}
console.log(offerDataArray);
