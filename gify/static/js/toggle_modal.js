const open = document.getElementById("open");
const modal_container = document.getElementById("modal_container");
const close = document.getElementById("close");


open.addEventListener("click", (event) => {
	event.preventDefault();
	modal_container.classList.add("show");
})

close.addEventListener("click", () => {
	modal_container.classList.remove("show");
})


const removeModal = (event) => {
	if (event.target.classList.contains("modal-post-container")) {
		modal_container.classList.remove("show");
	}
}

window.addEventListener("click", (event) => removeModal(event));
