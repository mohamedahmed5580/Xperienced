# API Documentation

## api/login
**Use:** logs the user into the system
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)
* username : string
* password : string

**Response:** (JSON)
* "error": error_message _(some data is missing or invalid username and/or password)_
* "success" : "User authenticated successfully" _(if all goes well)_

**Status Codes:** 400, 401, 200
<br>
**Example:**

```
fetch('api/login', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: username,
        password: password
    }),
}).then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message
    }
    else {
        // redirect
    }
});
```

## api/signup
**Use:** registers a new user and logs them into the system
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)
* first_name : string
* last_name : string
* username : string
* email: string
* phone: string
* password : string
* confirmation : string

**Response:** (JSON)
* "error": error_message _(some data is missing or invalid __see validation details bellow__)_
* "success" : "User authenticated successfully" _(if all goes well)_

**Error Codes:** 400, 401, 200
<br>
**Example:**

```
fetch('api/signup', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        // data speficified before
    }),
}).then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message
    }
    else {
        // redirect
    }
});
```

## api/verify_email/send
**Use:** sends an email verification token to the user's email (if not verified yet)
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)

**Response:** (JSON)
* "error": error_message _(user is not authenticated, email is already verified, or internal error)_
* "success" : "Token sent successfully" _(if all goes well)_

**Error Codes:** 400, 401, 403, 500, 200
<br>
**Example:**

```
fetch('api/verify_email/send', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
    }),
}).then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message
    }
    else {
        // display input field for the user to enter the token key
    }
});
```

## api/verify_email/verify
**Use:** verifies the user's email by sending the verification token to the user
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)
* token : integer

**Response:** (JSON)
* "error": error_message _(token is not correct, email is already verified, ...)_
* "success" : "Email verified successfully" _(if all goes well)_

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**

```
fetch('api/verify_email/verify', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        token: token
    }),
}).then(response => response.json()).then((response) => {
    // display message to the user
});
```

## api/new_request
**Use:** creates a new request
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)
* request: {"title", "description", "category", "budget",}

**Response:** (JSON)
* "error": error_message _(some data is missing or invalid __see valodation bellow__)_
* "request_id" : the id of the newly added request _(if all goes well)_

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**

```
fetch('api/new_request', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        request: request
    }),
}).then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message to the user
    }
    else {
        // redirect the user to the requests page ("requests/<request_id>")
    }
});
```

## api/requests
**Use:** fetches some __open__ requests from the server
<br>
**Method:** GET
<br>
**Request Parameters:** 
* [category : string] (optional)

**Response:** (JSON)
* "error": _if the specified category does not exist_
* "requests" : a list of request request {"owner", "title", "description", "requestCategory", "budget", "datetime"}


**Status Codes:** 400, 200
<br>
**Example:**

```
fetch('api/requests', {
    method: 'GET',
    body: JSON.stringify({
        categoty: "Computer Science"
    }),
});
// display requests
```

## api/requests/categories
**Use:** fetches all request categories along side their type
<br>
**Method:** GET
<br>
**Request Parameters:** 

**Response:** (JSON)
* "categories" : a list of category {"name", "requestType"}


**Status Codes:** 200
<br>
**Example:**

```
fetch('api/requests/categories').then(response => response.json()).then(response => {
    // do stuff
});
```

## api/requests/<int:id>
**Use:** fetches a request from the server
<br>
**Method:** GET
<br>
**Request Parameters:**

**Response:** (JSON)
* "error": "Request doesn't exist."
* "offers" : request {"owner", "title", "description", "requestCategory", "budget", "currentState", "datetime"}
**Status Codes:** 400, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>')
.then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/requests/<int:id>/offers
**Use:** fetches all offers that have been made on the specified request
<br>
**Method:** GET
<br>
**Request Parameters:**

**Response:** (JSON)
* "error": "Request doesn't exist."
* "offers" : _list of offers each has the following attributes: bidder, bid, notes, state_
**Status Codes:** 400, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/offers')
.then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/requests/<int:id>/cancel
**Use:** cancels a request that the user has made before (must be open/pending)
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)

**Response:** (JSON)
* "error": error_message _(request isn't owned by the user or request isn't open/pending)_
* "success" : "Request cancelled successfully" _(if all goes well)_

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/cancel', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
}).then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/requests/<int:id>/complete
**Use:** complete a request that is currently pending (the user accepted an offer)
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)

**Response:** (JSON)
* "error": error_message _(request isn't owned by the user or request isn't pending)_
* "success" : "Request completed successfully" _(if all goes well)_

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/complete', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
    }),
}).then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/requests/<int:id>/offers
**Use:** gets the offers that have been made to the request so far
<br>
**Method:** GET
<br>
**Request Parameters:** 

**Response:** (JSON)
* "error": "Request doesn't exist"
* "offers" : offers {"bidder", "bid", "notes", "state", "datetime"} _(if all goes well)_

**Status Codes:** 400, 401, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/offers')
.then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/requests/<int:id>/offers/add
**Use:** makes an offer to a specific request
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)
* offer: {"bid", "notes"}

**Response:** (JSON)
* "error": _user isn't allowed to make an offer or some data is missing/invalid __see validation details bellow___
* "success": "Offer added successfully"

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/offers/add', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        offer: offer
    }),
}).then(response => response.json()).then(response => {
    // display message to the user
});

```

## api/requests/<int:id>/offers/<int:offer_id>
**Use:** get the details of a specific offer
<br>
**Method:** GET
<br>
**Request Parameters:** 
* CSRF Token : string (header)

**Response:** (JSON)
* "error": _(request or offer doesn't exist)_
* "offer" : offer {"bidder", "bid", "notes", "state", "datetime"} _(if all goes well)_

**Status Codes:** 400, 401, 200
<br>
**Example:**

```
fetch('api/login')
.then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/requests/<int:id>/offers/<int:offer_id>/accept
**Use:** accepts a specific offer that the user received on their request
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)

**Response:** (JSON)
* "error": _request or offer doesn't exist, the user isn't authorized..._
* "success" : "Offer accepted successfully" _(if all goes well)_

**Status Codes:** 400, 401, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/offers/<int:offer_id>/accept', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
    }),
}).then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/requests/<int:id>/offers/<int:offer_id>/cancel
**Use:** cancel a specific offer that the user made to someone's request 
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)

**Response:** (JSON)
* "error": _request or offer doesn't exist, the user isn't authorized..._
* "success" : "Offer cancelled successfully" _(if all goes well)_

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**
```
fetch('api/login', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: username,
        password: password
    }),
}).then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message
    }
    else {
        // redirect
    }
});
```

## api/requests/<int:id>/chat (websockets will be used in the future)
**Use:** get all chat messages in a specific chatroom related to a specific request
<br>
**Method:** GET
<br>
**Request Parameters:** 
* CSRF Token : string (header)

**Response:** (JSON)
* "error": _user isn't authorized..._
* "messages" : messages [{"sender", "content", "read", "timestamp"}] _(if all goes well)_

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/chat')
.then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message
    }
    else {
        // display chat messages
    }
});
```

## api/requests/<int:id>/chat/send (websockets will be used in the future)
**Use:** sends a messages in a chat room
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)
* content: string

**Response:** (JSON)
* "error": _content is missing, user is not authorized..._
* "success" : "Message sent successfully" _(if all goes well)_

**Status Codes:** 400, 401, 403, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/chat/send', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        content: content
    }),
}).then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message
    }
    else {
        // display message or reload the page
    }
});
```

## api/profile/<str:username>
**Use:** gets some details about a profile
<br>
**Method:** GET
<br>
**Request Parameters:** 

**Response:** (JSON)
* "error": "profile doesn't exist"
* "profile" : profile {"username", "first_name", "last_name", "about", "skills" : []} _(if all goes well)_

**Status Codes:** 400, 200
<br>
**Example:**

```
fetch('api/profile/<str:username>')
.then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/profile/
**Use:** get all the details about the user's own profile
<br>
**Method:** GET
<br>
**Request Parameters:** 

**Response:** (JSON)
* "error": _user isn't loged in_
* "profile" : profile {"username", "first_name", "last_name", "email", "phone", "about", skills": [], "availableBalance", "onHoldBalance", "totalBalance"} _(if all goes well)_

**Status Codes:** 401, 200
<br>
**Example:**
```
fetch('api/profile')
.then(response => response.json()).then((response) => {
    // do stuff
});
```

## api/profile/edit
**Use:** edit some personal details
<br>
**Method:** POST
<br>
**Request Parameters:** 
* CSRF Token : string (header)
["first_name" : string] (optional)
["second_name : string"] (optional)
["about" : string] (optional)
["phone": string] (optional)
["email": string] (optional)
["skills": []] (optional)

**Response:** (JSON)
* "error": _user isn't logged in or some data is invalid __see valodation details bellow___
* "success" : "Profile edited successfully"

**Status Codes:** 400, 200
<br>
**Example:**

```
fetch('api/requests/<int:id>/chat/send', {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        // some of the data specified before
    }),
}).then(response => response.json()).then((response) => {
    if ("error" in response) {
        // display error message
    }
    else {
        // redirect
    }
});
```

## api/notifications
**Use:** get all notifications
<br>
**Method:** GET
<br>
**Request Parameters:** 

**Response:** (JSON)
* "error": _user isn't logged in_
* "notifications" : notifications [{"content", "url", "read", "timestamp"}]

**Status Codes:** 401, 200
<br>
**Example:**

```
fetch('api/notifications')
.then(response => response.json()).then((response) => {
    // display notifications
});
```

## api/messages
**Use:** get all messages
<br>
**Method:** GET
<br>
**Request Parameters:** 

**Response:** (JSON)
* "error": _user isn't logged in_
* "messages" : messages [{"content", "sender", "read", "timestamp", "request_id"}]

**Status Codes:** 401, 200
<br>
**Example:**

```
fetch('api/messages')
.then(response => response.json()).then((response) => {
    // display messages
});
```