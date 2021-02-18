const open = document.getElementById("open");
const modal_container = document.getElementById("modal_container");
const close = document.getElementById("close_modal");
const form = document.getElementById("new-post-form");
const url = document.getElementById("link_url");
const urlerror = document.querySelector("#link_url + span.errorurl");


/*
 * Open modal on click event
 */
open.addEventListener("click", (event) => {
	event.preventDefault();
	modal_container.classList.add("show");
})


/*
 * Function handling modal removal.
 * If click was registered outside modal container close modal
 */
const removeModal = (event) => {
	if (event.target.classList.contains("modal-post-container")) {
		modal_container.classList.remove("show");
	}
}


/*
 * Event listener for checking validity of link input field
 */
url.addEventListener("input", event => {
	if (url.validity.valid) {
		urlerror.textContent = "";
		urlerror.className = "errorurl";
	} else {
		showError();
	}
})


/*
 * Display errors under 'link' input field
 */
const showError = () => {
	if (url.validity.valueMissing) {
		urlerror.textContent = "You need to enter video URL";
	} else if (url.validity.typeMismatch) {
		urlerror.textContent = "Cannot detect valid URL";
	} else if (url.validity.patternMismatch) {
		urlerror.textContent = "Only youtube and streamable links are currently supported";
	}
	urlerror.className = "errorurl active";
}


/*
 * Event listener for handling post form submission
 */
form.addEventListener("submit", event => {
	event.preventDefault();
	if (!url.validity.valid) {
		showError();
	} else {
		uploadURL();
	}
})


/*
 * Function for handling form upload process.
 * Handle any errors returned from the server
 */
const uploadURL = async () => {
	const link = url.value;
    const csrfToken = getCookie("csrftoken");
	const response = await fetch("/create/", {
		method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
		body: new URLSearchParams({
			"link": link
		}),
	})
	const responseJson = await response.json()
	if (responseJson.status == "error") {
		const errorArray = handleFormErrors(responseJson);
		displayErrorsOnForm(errorArray);
	}
	
	return response;
}


/*
 * Retrieve all errors returned by the server-side validation
 * for the 'link' input field
 */
const handleFormErrors = (responseJson) => {
	errors = JSON.parse(responseJson.errors).link;
	let errorArray = [];
	for (const error of errors) {
		errorArray.push(error.message);
	}
	
	return errorArray;
}


/*
 * Receive list of all errors returned from server
 * and display them on the form
 */
const displayErrorsOnForm = (errorArray) => {
	urlerror.className = "errorurl active";
	for (const message of errorArray) {
		urlerror.textContent = message;
	}
}


window.addEventListener("click", (event) => removeModal(event));
