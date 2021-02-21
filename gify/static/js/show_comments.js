const template = document.getElementById('add-comment');


document.body.addEventListener('click', event => {
	if (event.srcElement.className === 'comment_button') {
		const clone = document.importNode(template.content, true);
		const postDiv = getPostDiv(event.target);
		console.log(postDiv);
	}
})


/*
 * Receives clicked on button
 * and returns its parent 'post' div
 */
const getPostDiv = (element) => {
	// Search for parent post div up to 'height' elements in DOM
	let height = 4;
	while (height > 0) {
		element = element.parentNode;
		if (element.className.includes('card post')) {
			return element;
		}
		height--;	
	}
}
