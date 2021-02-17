const open = document.getElementById("open");
const modal_container = document.getElementById("modal_container");
const close = document.getElementById("close_modal");
const form = document.getElementById("new-post-form");


open.addEventListener("click", (event) => {
	event.preventDefault();
	modal_container.classList.add("show");
})

const removeModal = (event) => {
	if (event.target.classList.contains("modal-post-container")) {
		modal_container.classList.remove("show");
	}
}

window.addEventListener("click", (event) => removeModal(event));

const url = document.getElementById("link_url");
const urlerror = document.querySelector("#link_url + span.errorurl");

url.addEventListener("input", event => {
	if (url.validity.valid) {
		urlerror.textContent = "";
		urlerror.className = "errorurl";
	} else {
		showError();
	}
})

form.addEventListener("submit", event => {
	if (!url.validity.valid) {
		showError();
		event.preventDefault();
	} else {
		// Submit form
	}
})

const showError = () => {
	if (url.validity.valueMissing) {
		urlerror.textContent = "You need to enter video URL";
	} else if (url.validity.typeMismatch) {
		urlerror.textContent = "Entered value needs to be an URL";
	}
	urlerror.className = "errorurl active";
}
