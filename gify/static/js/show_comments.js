/*
 * Check if 'comment' button was clicked and 
 * display all comments for a given post
 */
document.body.addEventListener('click', event => {
	if (event.srcElement.className === 'comment_button') {
		const postDiv = getPostDiv(event.target);
		const addComment = postDiv.querySelector('.add-new-post');
		const SHOW_COMMENT = 'showcomment';
		const HIDE_COMMENT = 'hideComment';

		if (addComment.style.animationName == SHOW_COMMENT) {
			addComment.classList.toggle(HIDE_COMMENT);
		} else {
			addComment.style.animationName = SHOW_COMMENT;
			addComment.style.animationPlayState = 'running';
		}


	}
})


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
