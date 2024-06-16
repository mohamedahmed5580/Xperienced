var AccountDataArray = JSON.parse(localStorage.getItem('AccountDataArray')) || [];

function addAccount() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const email = document.getElementById('email').value;
    const companyName = document.getElementById('companyiO').value;

    const accountData = {
        username: username,
        password: password,
        confirmPassword: confirmPassword,
        email: email,
        isCompany: document.getElementById('myCheckbox').checked,
        companyName: companyName
    };

    AccountDataArray.push(accountData);
    $.ajax({
        type: 'POST',
        url: '/api/signup/', // Ensure this URL is correct
        data: JSON.stringify(accountData),
        contentType: 'application/json',
        success: function(response) {

            console.log('Signup successful');
        },
        error: function(xhr, status, error) {
            // Handle error response
            console.error('Error occurred:', error);
        }
    });
    window.localStorage.setItem('AccountDataArray', JSON.stringify(AccountDataArray));
    // saveDataInFile(accountData, 'Account_data.json');
    // window.location.href = "index.html";
}

// const fs = require('fs'); // Import the fs module

const saveDataInFile = (data, file) => {
    const finished = (error) => {
        if (error) {
            console.error(error);
            throw error; // Throw the error to stop the execution
        }
    }
    let AccountData = JSON.stringify(data, null, 2);
    fs.writeFile(file, AccountData, finished);
}
function gotouser() {
    var user = document.getElementById("username").value.toLowerCase();
    var pass = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;
    var found = false;

    if (AccountDataArray.length === 0) {
        console.log("No accounts found.");
        return;
    }

    for (var i = 0; i < AccountDataArray.length; i++) {
        if (AccountDataArray[i].username.toLowerCase() === user && AccountDataArray[i].password === pass && AccountDataArray[i].confirmPassword === confirmPassword) {
            found = true;
            break;
        }
    }

    if (found) {
        window.location.href = "index.html";
    } else {
        console.log("Invalid username or password.");
    }
}

console.log(AccountDataArray);