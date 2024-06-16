var jobDataArray = JSON.parse(localStorage.getItem('jobDataArray')) || [];

 function addJob() {
     // Get user input values
    
     var title = document.getElementById("title").value;
     var salary = document.getElementById("salary").value;
     var companyName = document.getElementById("company-name").value;
     var jobStatus = document.getElementById("job-status").value;
     var openClosed=document.getElementById("o_p").value;
     var description = document.getElementById("description").value;
     var yearsOfExperience = document.getElementById("years-of-experience").value;
     var jobID=document.getElementById("jobID").value;

     // Create job object
     var jobData = {
        
        title: title,
        salary: salary,
        company_name: companyName,
        job_status: jobStatus,
        description: description,
        open_closed: openClosed,
        years_of_experience_required: yearsOfExperience,
        job_id:jobID
    };
     // Add job to the array
     jobDataArray.push(jobData);

     // Store job data array in local storage
     localStorage.setItem('jobDataArray', JSON.stringify(jobDataArray));

     // Update JSON file content and allow the user to download the updated JSON file
     updateJSONFile();
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

 function displayJobs() {
    var jobListItems = document.getElementById("job-list-items");
    jobListItems.innerHTML = "";

    jobDataArray.forEach(function(jobData, index) {
        var listItem = document.createElement("div");
        listItem.innerHTML = `
            <div class="jobs">
                <div class="job-item">
                    <img src="../images/job.jpg" alt="${jobData.title} photo" >
                    <span>${jobData.open_closed}</span>
                    <h3 class="job-title">${jobData.title}</h3>
                    <div class="job-info">
                        <details>
                            <summary><b>Main Info</b></summary>
                            <p>Salary: ${jobData.salary}</p>
                            <p>Company Name: ${jobData.company_name}</p>
                            <p>Job Status: ${jobData.job_status}</p>
                            <p>Years of Experience Required: ${jobData.years_of_experience_required}</p>
                        </details>
                    </div>
                    <div class="job-description">
                        ${jobData.description}
                    </div>
                    <div class="apply-btn">
                    <button id="apply_${jobData.job_id}">Apply Now</button>
                    </div>
                </div>
            </div>
        `;
        jobListItems.appendChild(listItem);
    });

    // Add event listeners
    document.addEventListener('click', function(event) {
        if (event.target && event.target.id.startsWith('apply_')) {
            var jobId = event.target.id.split('_')[1];
            localStorage.setItem('appliedJobId', jobId);
            window.location.assign('apply-form.html');
        }
    });
    
 }
displayJobs();