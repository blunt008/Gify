document.body.addEventListener('click', event => {
	if (event.srcElement.className === 'comment_button') {
		console.log('shows comments');
	}
})
