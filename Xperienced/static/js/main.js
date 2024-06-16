window.getJobDataById = function(jobID) {
    // Retrieve the job data array from localStorage
    var jobs = JSON.parse(localStorage.getItem('jobDataArray')) || [];

    // Find the job object with the specified ID
    var foundJob = jobs.find(job => job.job_id === jobID);

    // Return the found job object or null if not found
    return foundJob || null;
};


function applyJob(jobID) {
    console.log("Applying for job with ID:", jobID); // Log the job ID to verify it's received correctly

    // Get the job data based on the ID (using globally accessible getJobDataById)
    var job = getJobDataById(jobID);

    if (job) {
        console.log("Job data to be saved:", job); // Log the job data to verify it's correct

        // Save the job data to localStorage
        saveAppliedJob(job);
    } else {
        console.log("No job found with ID:", jobID);
    }
}

function saveAppliedJob(job) {
    console.log("Saving job data:", job); // Log the job data to verify it's being saved correctly
    localStorage.setItem('appliedJob', JSON.stringify(job));
}

function displayAppliedJob() {
    try {
        var appliedJobId = localStorage.getItem('appliedJobId');
        if (appliedJobId) {
            // Get the applied job data based on the stored job ID
            var appliedJob = getJobDataById(appliedJobId);
            if (appliedJob) {
                // Display the applied job details
                var appliedd1 = document.getElementById("appliedd");
               
                var jobInfo = document.createElement("div");
                jobInfo.classList.add("job-info");
                jobInfo.innerHTML = `
                <div class="applied-jobs-d">
                      <div class="applied-jobs-items">
                      <img  class="im"src="../images/job.jpg" alt="${appliedJob.title} photo" >
                      
                      <h3 class="a-job-title">${appliedJob.title}</h3>
                      <div class="a-job-info">
                      <details>
                          <summary><b>Main Info</b></summary>
                          <p>Salary: ${appliedJob.salary}</p>
                          <p>Company Name: ${appliedJob.company_name}</p>
                        
                          <p>Years of Experience Required: ${appliedJob.years_of_experience_required}</p>
                      </details>
                  </div>
                  <div class="a-job-description">
                      ${appliedJob.description}
                  </div>
                  </div>
                  </div>
                `;
                appliedd1.appendChild(jobInfo);
            } else {
                console.error("No applied job found with ID:", appliedJobId);
            }
        } else {
            console.error("No applied job ID found in local storage.");
        }
    } catch (error) {
        console.error("Error retrieving applied job:", error);
    }
}

displayAppliedJob();
