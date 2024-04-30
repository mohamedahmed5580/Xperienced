var offerDataArray = JSON.parse(localStorage.getItem('offerDataArray')) || [];
var btn=document.getElementById("btnAdd");
btn.onclick = function() {
    var title = document.getElementById("title").value;
    var salary = document.getElementById("salary").value;
    var skills = document.getElementById("skills").value;
    var type = document.getElementById("type").value;
    var description = document.getElementById("description").value;
    var type = document.getElementById("type").value;
    var category = document.getElementById("category").value;
    if (title.value =='') {
      this.contains= 'Please enter a title';
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
    
    }
   
}

  
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