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
        modal_container.style.opacity = null;
        modal_container.classList.add("show");
    })
}


/*
 * Function handling modal removal.
 * If click was registered outside modal container close modal
 */
const removeModal = () => {
    modal_container.classList.remove("show");
    modal_container.style.opacity = '0';
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
    const csrfToken = Cookies.get("csrftoken");

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
 * Show new comment input and post comments
 */
const enableComments = (event) => {
    const postDiv = getPostDiv(event.target);
    const commentForm = postDiv.querySelector('.new-comment-form');

    displayCommentInput(postDiv);
    displayPostComments(postDiv);
    removeClickEvent(postDiv);

    commentForm.addEventListener('submit', addNewComment);
}


/*
 * Like or unlike clicked post
 */
const likeDislike = event => {
    const button = event.target;

    button.classList.toggle('liked');
};


/*
 * Retrieve and display comments
 */
const displayPostComments = async (postDiv) => {
    const postID = postDiv.dataset.id;
    const postsContainer = postDiv.querySelector('.comments-container');
    const csrfToken = Cookies.get('csrftoken');

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

    addComment.style.display = 'flex';
    addComment.style.animationName = 'showcomment';
    addComment.style.animationPlayState = 'running';
}


/*
 * Receives clicked button
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


/*
 * Remove 'click' event listener from comment button
 */
const removeClickEvent = (postDiv) => {
    const commentButton = postDiv.querySelector('.comment_button');
    commentButton.removeEventListener('click', enableComments);
}


const addNewComment = async (event) => {
    event.preventDefault();
    const csrfToken = Cookies.get('csrftoken');
    const commentInput = event.target.querySelector('.new-comment-input');
    const commentBody = commentInput.value;
    const postDiv = getPostDiv(event.target);
    const postID = postDiv.dataset.id;

    const response = await fetch('comment/add/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'body': commentBody,
            'post_id': postID
        })
    })

    if (!response.ok) {
        handleCommentFormErrors(commentInput);
    } else if (response.ok) {
        const responseJson = await response.json();
        handleCommentFormValid(responseJson, commentInput);
    }
}


const handleCommentFormValid = (response, input) => {
    const comment = response.comment
    const created = getLocalDate(comment.created);
    const author = comment.author;
    const body = comment.body;
    const postDiv = getPostDiv(input);
    const commentsContainer = postDiv.querySelector('.comments-container');

    input.value = '';
    addCommentToPost(author, created, body, commentsContainer);
};


const addCommentToPost = (author, date, body, container) => {
    const comments = container.querySelectorAll('.post-comment');
    const commentTemplate = document.getElementById('comment-template');
    const content = document.importNode(commentTemplate.content, true);
    const post = content.querySelector('.post-comment');
    let authorParagraph = content.querySelector('.comment-author');
    let dateSpan = content.querySelector('.comment-date');
    let bodyParagraph = content.querySelector('.comment-body');

    authorParagraph.textContent = `${author} at `;
    dateSpan.textContent = date;
    authorParagraph.appendChild(dateSpan);
    bodyParagraph.textContent = body;
    post.classList.toggle('animateNewCommentAdd');

    if (comments) {
        container.insertBefore(content, comments[0]);
    } else {
        container.appendChild(content);
    }

};


const getLocalDate = (date) => {
    const localDate = new Date(date);
    const options = { month: 'long', day: '2-digit', year: 'numeric', hour12: true, hour: 'numeric', minute: '2-digit' };

    return localDate.toLocaleString('en-US', options);
};


/*
 * Toggle on/off red border around new comment input
 */
const handleCommentFormErrors = (commentInput) => {
    commentInput.classList.toggle('new-comment-error');
    setTimeout(() => {
        commentInput.classList.toggle('new-comment-error');
    }, 1500)
}


window.addEventListener('DOMContentLoaded', event => {
    document.addEventListener('click', event => {
        if (event.target.matches('.comment_button')) {
            enableComments(event);
        }

        if (event.target.matches('.like_button')) {
            likeDislike(event);
        }
    });
});
