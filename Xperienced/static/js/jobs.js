var jobDataArray = JSON.parse(localStorage.getItem('jobDataArray')) || [];


function addJob() {
    var title = document.getElementById("title").value;
    var salary = document.getElementById("salary").value;
    var companyName = document.getElementById("company-name").value;
    var jobStatus = document.getElementById("job-status").value;
    var description = document.getElementById("description").value;
    var yearsOfExperience = document.getElementById("years-of-experience").value;
    
    var jobData = {
        title: title,
        salary: salary,
        company_name: companyName,
        job_status: jobStatus,
        description: description,
        years_of_experience_required: yearsOfExperience
    };

    jobDataArray.push(jobData);

    window.localStorage.setItem('jobDataArray', JSON.stringify(jobDataArray));

}

  
function updateJSONFile() {
    var jsonData = JSON.stringify(jobDataArray);
    var blob = new Blob([jsonData], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'job_data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function gotouser() {
    var user = document.getElementById("username").value;
    var pass = document.getElementById("password").value;
    if (user == 'user'|| pass=='user') {
        window.location.href = "User/user-page.html";
    }else{
        window.location.href = "index.html";
    }
}
console.log(jobDataArray);