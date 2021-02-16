const comments = document.querySelectorAll(".comment_button");



const test = (event) => {
	console.log(event);
}


comments.forEach(comment => comment.addEventListener("click", test));
