var jobDataArray = JSON.parse(localStorage.getItem('jobDataArray')) || [];

function dspliayJobs() {
    var jobListItems = document.getElementById("job-list-items");
    jobDataArray.forEach(function(jobData, index) {
        var listItem = document.createElement("div");
        listItem.innerHTML = `
        <div class="coloumn">
        <div class="images">
          <img src="{% static 'images/your-image.jpg' %}">
        </div>
        <div class="text" >
          <h3>${jobData.title}</h3>
          <h5>${jobData.company_name}</h5>
          <p>
          ${jobData.description}
          </p>
          <div class="btns">
          <button id="btnAddjob" type="submit" onclick="removeJob(${index})">Remove Job</button>
          <button id="btnAddjob" type="submit" >Edit Job</button>

          </div>
          
        </div>
                        
           
        `;
        jobListItems.appendChild(listItem);
    });
}
function removeJob(index) {
    jobDataArray.splice(index, 1);
    
    window.localStorage.setItem('jobDataArray', JSON.stringify(jobDataArray));
    window.location.reload();
}

dspliayJobs();




