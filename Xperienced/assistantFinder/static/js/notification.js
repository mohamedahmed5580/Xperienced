var notifications = [
    { title: "New Message Received", content: "You have received a new message from a client regarding your project.", date: "April 25, 2024" },
    { title: "Project Completed", content: "Congratulations! Your project has been successfully completed and approved by the client.", date: "April 24, 2024" },
    { title: "New Proposal", content: "You have received a new proposal from a freelancer for your project.", date: "April 23, 2024" },
    { title: "Payment Received", content: "You have received a payment for your completed work.", date: "April 22, 2024" },
    { title: "Project Updated", content: "Your project has been updated by the client. Please review the changes.", date: "April 21, 2024" },
    { title: "New Feedback", content: "You have received new feedback on your completed project.", date: "April 20, 2024" },
    { title: "Project Awarded", content: "Congratulations! Your proposal has been accepted and the project has been awarded to you.", date: "April 19, 2024" },
    { title: "New Milestone Created", content: "A new milestone has been created for your project. Please review and approve it.", date: "April 18, 2024" },
    { title: "Milestone Completed", content: "One of the milestones in your project has been completed. Please review and approve it.", date: "April 17, 2024" },
    { title: "Project Deadline Extended", content: "The deadline for your project has been extended. Please check the new timeline.", date: "April 16, 2024" },
    { title: "New Task Assigned", content: "You have been assigned a new task on your project. Please review it and take necessary action.", date: "April 15, 2024" },
    { title: "Task Completed", content: "One of the tasks assigned to you has been completed. Please review and approve it.", date: "April 14, 2024" },
    { title: "New Order Placed", content: "A new order has been placed for your services. Please review and take necessary action.", date: "April 13, 2024" },
    { title: "Order Shipped", content: "Your order has been shipped and is on its way. You will receive it soon.", date: "April 12, 2024" },
    { title: "New Review Received", content: "You have received a new review for your services. Please review and respond.", date: "April 11, 2024" },
    { title: "Profile Updated", content: "Your profile information has been updated successfully.", date: "April 10, 2024" },
    { title: "New Project Posted", content: "A new project matching your skills has been posted. Please review and submit your proposal.", date: "April 9, 2024" },
    { title: "Project Closed", content: "The project you were working on has been closed. Thank you for your contribution.", date: "April 8, 2024" },
    { title: "New Message Sent", content: "You have successfully sent a new message to a client regarding your project.", date: "April 7, 2024" },
    { title: "New Order Received", content: "You have received a new order for your services. Please review and take necessary action.", date: "April 6, 2024" },
    { title: "Order Delivered", content: "Your order has been delivered successfully to the client.", date: "April 5, 2024" },
    { title: "New Bid Placed", content: "You have successfully placed a new bid on a project. Please wait for the client's response.", date: "April 4, 2024" },
    { title: "Bid Accepted", content: "Congratulations! Your bid on a project has been accepted by the client.", date: "April 3, 2024" },
    { title: "New Task Created", content: "A new task has been created for your project. Please review and take necessary action.", date: "April 2, 2024" },
    { title: "Task Updated", content: "One of the tasks in your project has been updated. Please review the changes.", date: "April 1, 2024" },
    { title: "New Message Received", content: "You have received a new message from a client regarding your project.", date: "April 25, 2024" },
 // أضف المزيد من الإشعارات هنا
];

var currentPage = 1;
var notificationsPerPage = 20;

function displayNotifications(page) {
    var startIndex = (page - 1) * notificationsPerPage;
    var endIndex = startIndex + notificationsPerPage;
    var notificationsToShow = notifications.slice(startIndex, endIndex);

    var notificationsContainer = document.getElementById('notifications-container');
    notificationsContainer.innerHTML = ''; // Clear previous notifications

    notificationsToShow.forEach(function(notification) {
        var notificationElement = document.createElement('div');
        notificationElement.classList.add('notification-contents');
        notificationElement.innerHTML = `
            <p class="notification-title">${notification.title}</p>
            <p class="notification-contents">${notification.content}</p>
            <p class="notification-date">${notification.date}</p>
        `;
        notificationsContainer.appendChild(notificationElement);
    });
}

function displayPagination() {
    var totalNotifications = notifications.length;
    var totalPages = Math.ceil(totalNotifications / notificationsPerPage);
    var paginationContainer = document.getElementById('btn-group');
    paginationContainer.classList.add('center');

    for (var i = 1; i <= totalPages; i++) {
        var button = document.createElement('input');
        button.classList.add('btn-check');
        button.classList.add('btn-check');
        button.type = 'radio';
        button.id = 'btnradio' + i;
        button.name = 'btnradio';
        button.value = i; 
        button.addEventListener('click', function() {
            currentPage = parseInt(this.value);
            displayNotifications(currentPage);
        });
        var label = document.createElement('label');
        label.setAttribute('for', 'btnradio' + i);
        label.textContent = i;
        label.classList.add('btn', 'btn-outline-primary');
        paginationContainer.appendChild(button);
        paginationContainer.appendChild(label);
    }

}

displayNotifications(currentPage);
displayPagination();
