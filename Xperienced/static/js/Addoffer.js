
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

console.log(offerDataArray);

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