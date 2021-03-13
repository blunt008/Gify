const open = document.getElementById("open");
const modal_container = document.getElementById("modal_container");
const close = document.getElementById("close_modal");
const form = document.getElementById("new-post-form");
const url = document.getElementById("link_url");
const urlerror = document.querySelector("#link_url + span.errorurl");


/*
 * Open modal on click event
 */
if (open) {
	open.addEventListener("click", (event) => {
		event.preventDefault();
		url.value = "";
		modal_container.classList.add("show");
	})
}


/*
 * Function handling modal removal.
 * If click was registered outside modal container close modal
 */
const removeModal = () => {
	modal_container.classList.remove("show");
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

	if (!response.ok) {
		const responseJson = await response.json();
		const errorArray = handleFormErrors(responseJson);
		displayErrorsOnForm(errorArray);
	}

	if (response.ok) {
		responseJson = await response.json()
		createPost(responseJson.link, responseJson.id);
		removeModal();
	}
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


/*
 * Create post
 */
const createPost = (link, id) => {
    const container = document.getElementById("container");
	const postTemplate = document.getElementById("post-template");
	const content = document.importNode(postTemplate.content, true);
	const iframe = content.querySelector("iframe");
	const post = content.querySelector('.post');
	const posts = document.querySelectorAll(".post");

	iframe.src = link;
	iframe.setAttribute('allowfullscreen', true);

	post.dataset.id = id;

	if (posts.length > 0) {
		container.insertBefore(content, posts[0]);
	} else {
		container.appendChild(content);
	}

	addEventListenerToComment();
}


/*
 * Remove modal on click event inside modal container
 */
window.addEventListener("click", (event) => {
	if (event.target.classList.contains("modal-post-container")) {
		removeModal();
	}
});


/*
 * Attach event listener to each comment button
 */
const addEventListenerToComment = () => {
	const comments = document.querySelectorAll('.comment_button');
	comments.forEach(comment => addEventListener('click', enableComments));
}


/*
 * Show new comment input and post comments
 */
const enableComments = (event) => {
	const postDiv = getPostDiv(event.target);
	
	displayCommentInput(postDiv);
	displayPostComments(postDiv);
}


/*
 * Retrieve and display comments
 */
const displayPostComments = async (postDiv) => {
	const postID = postDiv.dataset.id;
	const postsContainer = postDiv.querySelector('.comments-container');
	const csrfToken = getCookie('csrftoken');

	const response = await fetch(`/get_comments?post=${postID}`, {
		method: 'GET',
		headers: {
			'X-CSRFToken': csrfToken,
		},
	})

	const responseText = await response.text();

	postsContainer.insertAdjacentHTML('afterbegin', responseText);
}


/*
 * Display new comment input for a given post
 */
const displayCommentInput = (postDiv) => {
	const addComment = postDiv.querySelector('.add-new-post');

	addComment.style.animationName = 'showcomment';
	addComment.style.animationPlayState = 'running';
}


/*
 * Receives clicked on button
 * and returns its parent 'post' div
 */
const getPostDiv = (element) => {
	let height = 4;
	while (height > 0) {
		element = element.parentNode;
		if (element.className.includes('card post')) {
			return element;
		}
		height--;	
	}
}


addEventListenerToComment();
