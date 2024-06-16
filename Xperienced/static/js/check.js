
var btnc =document.getElementById('myCheckbox').addEventListener('change', checkboxClicked);

function checkboxClicked() {
    var checkbox = document.getElementById('myCheckbox');

    if (checkbox.checked) {
        document.getElementById('companyO').classList.add('company');
        document.getElementById('companyO').classList.remove('companyO');
        document.getElementById('companyiO').classList.add('company');
        document.getElementById('companyiO').classList.remove('companyO');
        

    } else {
        document.getElementById('companyO').classList.add('companyO');
        document.getElementById('companyO').classList.remove('company');
        document.getElementById('companyiO').classList.add('companyO');
        document.getElementById('companyiO').classList.remove('company');
    }
}
