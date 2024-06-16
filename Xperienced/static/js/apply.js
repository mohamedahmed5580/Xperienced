const form = document.getElementById('form') ;
const firstName = document.getElementById('first') ;
const lastName = document.getElementById('last') ;
const email = document.getElementById('emaiil') ;
const phone = document.getElementById('phhone') ;
const lastComapany = document.getElementById('lstcompany') ;
const date = document.getElementById('date') ;
const address = document.getElementById('address') ;
const zipCode = document.getElementById('zipcode') ;
const city = document.getElementById('city') ;
const comments = document.getElementById('comments') ;
const appLetter = document.getElementById('appletter') ;
const cv = document.getElementById('cv') ;
const inputs = form.querySelectorAll("input[type = 'text']") ;
form.addEventListener('submit', e => {
    e.preventDefault();

    validateInputs();
});
form.addEventListener("file" , e => {
    e.preventDefault() ;
});
let popup = document.getElementById("popup") ;
function openpopup(){
    popup.classList.add("open-popup") ;

}
function closepopup(){
    popup.classList.remove("open-popup") ;

}
console.log(document.getElementById("form"));
const setError = (Element , message) => {
    const inputControl = Element.parentElement ;
    inputControl.querySelector(".error") ;
    inputControl.classList.add('error') ;
    inputControl.classList.remove('success') ;
};
const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');
    if(errorDisplay){
        errorDisplay.innerText = '' ;
    }
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};
const isValidEmail = email => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
const isValidPhoneNumber = phone => {
   const re = /^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/; 
   return re.test(String(phone)) ; 
} ;
function isValidDate(date) {
    return !isNaN((Date(date))) ;
}
const validateInputs = () => {
    const FirstName = firstName.value.trim() ;
    const LastName = lastName.value.trim() ;
    const Email =email.value.trim() ;
    const Phone = phone.value.trim() ;
    const LastComapany = lastComapany.value.trim() ;
    const Date = date.value.trim() ;
   
    if(FirstName === ''){
        setError(firstName , 'First Name is Rqquired') ;
    }
    else{
        setSuccess(firstName) ;
    } 
    if(LastName === ''){
        setError(lastName , 'Last Name is Rqquired') ;
    }
    else{
        setSuccess(lastName) ;
    } 
    if(Email === ''){
        setError(email , 'Email is Required') ;
    }
    else if(!isValidEmail(Email)){
        setError(email , 'Provide a valid Email address') ;

    }
    else {
        setSuccess(email) ;
    }  
    if(phone === ''){
        setError(phone , 'Phone Number is Rqquired') ;
    } 
    else if(!isValidPhoneNumber(Phone)) {
        setError(phone , 'Provide a valid Phone Number') ;
    } 
    else {
        setSuccess(phone) ;
    } 
    if(LastComapany === ''){
        setError(lastComapany , 'Last Company you worked for is Required') ;
    } 
    else {
        setSuccess(lastComapany) ;
    }
    if(!isValidDate(Date)){
        setError(date , 'Provide a valid Date') ;
    }
    else {
        setSuccess(date) ;
    } 
    openpopup() ;
    if (!document.querySelector('.error')) {
        form.submit(); // This will trigger the form submission
        console.log("Form submitted successfully.");
    }
}
form.addEventListener('submit', e => {
    e.preventDefault();
    validateInputs(); // Validate and then maybe submit inside this function

    // If validations pass, then process the job application
   // Retrieve the job ID from local storage
var jobId = localStorage.getItem('applyingForJobId');

// Check if the job ID exists
if (jobID) {
    // Call applyJob function with the retrieved job ID
    applyJob(jobID); // Assuming applyJob is accessible globally or you redirect to the job applied page with the jobId

    // Remove the stored job ID from session stora
    localStorage.removeItem('applyingForJobId'); // Clear the stored job ID
} else {
    // Log an error if no job ID is found
    console.error('No job ID found');
}

});




