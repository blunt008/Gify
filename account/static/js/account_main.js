const userAvatar = document.getElementById("avatar-main-edit-default");
const saveBtn = document.getElementById("save");
const closeModal = document.getElementById("close");


/*
 * Change source attribute of the main and nav avatar
 * close modal after
 */
const updateAvatar = (url) => {
    const navAvatar = document.getElementById("avatar-nav");

    navAvatar.src = url;
    userAvatar.src = url;

    closeModal.click();
};


/*
 * Change user's avatar to default one (no avatar)
 */
const switchToDefaultAvatar = () => {
    const navAvatar = document.getElementById("avatar-link");

    navAvatar.src = "/static/no-avatar.png";
    userAvatar.src = "/static/no-avatar.png";
    userAvatar.removeAttribute("data-toggle");
    userAvatar.removeEventListener("click", requestAvatars);
};


/*
 * Initialize and handle avatar deletion request
 */
const removeAvatar = (event, div, avatarCount) => {
    const csrfToken = getCookie("csrftoken");
    const avatarID = event.currentTarget.dataset.id;

    fetch("/account/delete_avatar/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "id": avatarID
        }),
        mode: "same-origin"
    })
        .then(response => {
            if (response.ok) {
                // Close modal if removed avatar was last avatar uploaded
                if (avatarCount === 1) {
                    closeModal.click();
                    switchToDefaultAvatar();
                }
                // Disable save button as well as remove div holding avatar
                saveBtn.disabled = true;
                saveBtn.ariaDisabled = "disabled";
                div.remove()
                return response.json()
            } else {
                return response.json()
            }
        })
        .then(response => {
            if (response.selected) {
                switchToDefaultAvatar()
            }
        })
}


/*
 * Retrieve csrfToken
 */
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};


/*
 * Retrieve all avatars available for user
 */
const requestAvatars = async (event) => {
    const csrfToken = getCookie("csrftoken");
    const profileID = event.target.dataset.id;

    // Fetch all avatars for the given user
    const response = await fetch("/account/avatars/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "id": profileID
        }),
        mode: "same-origin"
    });


    if (response.ok) {
        const responseJson = await response.json();
        const avatars = responseJson.avatars;
        displayAvatars(avatars);
    }
};


/*
 * Display all available avatars inside the modal
 */
const displayAvatars = (avatars) => {
    const modal = document.querySelector(".modal-body");
    const avatarCount = avatars.length;

    while (modal.firstChild) {
        modal.removeChild(modal.firstChild);
    }

    for (const avatar of avatars) {
        const div = document.createElement("div");
        const img = document.createElement("img");
        const deleteAvatarBtn = document.createElement("button");
        const deleteSpan = document.createElement("span");

        div.className = "avatar-preview-container";
        img.className = "avatar-preview";
        deleteAvatarBtn.className = "close hidden deleteAvatar";
        deleteAvatarBtn.ariaLabel = "Close";
        deleteAvatarBtn.type = "button";
        deleteAvatarBtn.dataset.id = avatar.id;
        deleteAvatarBtn.addEventListener("click", (event) => {
            removeAvatar(event, div, avatarCount);
        })
        deleteSpan.ariaHidden = "true";
        deleteSpan.innerHTML = "&times;";
        img.src = avatar.url;
        img.dataset.id = avatar.id;

        deleteAvatarBtn.appendChild(deleteSpan)
        div.appendChild(img);
        div.appendChild(deleteAvatarBtn)
        modal.appendChild(div);

        saveBtn.disabled = true;
        saveBtn.ariaDisabled = "disabled";
        div.addEventListener("click", (event) => selectAvatar(event));
    }
};


/*
 * Handle avatar selection inside the avatars modal
 */
const selectAvatar = (event) => {
    const avatars = document.querySelectorAll(".avatar-preview-container");
    const clickedTarget = event.currentTarget;
    const clickedTargetDeleteBtn = clickedTarget.querySelector(".close");
    const allDeleteButtons = document.querySelectorAll(".deleteAvatar");

    for (const deleteButton of allDeleteButtons) {
        if (!deleteButton.classList.contains("hidden")) {
            deleteButton.classList.add("hidden");
        }
    }
    for (const avatar of avatars) {
        if (avatar != clickedTarget) {
            avatar.classList.remove("selected");
        } else if (avatar === clickedTarget) {
            clickedTargetDeleteBtn.classList.toggle("hidden")
            clickedTarget.classList.add("selected");
        }
    }

    saveBtn.disabled = false;
    saveBtn.removeAttribute("aria-disabled");
};


/*
 * Check if user avatar is loaded on the page and if it is
 * add event handler to it
 */
if (userAvatar) {
    userAvatar.addEventListener("click", requestAvatars);
}


/*
 * Check if save button is loaded on the page and if it is
 * handle saving avatar logic
 */
if (saveBtn) {
    saveBtn.addEventListener("click", (event) => {
        const modal = document.querySelector(".modal");
        const avatars = document.querySelectorAll(".avatar-preview-container");
        const csrfToken = getCookie("csrftoken");
        let avatarSelected = false;
        let selectedAvatarID = 0;

        for (const avatar of avatars) {
            if (avatar.classList.contains("selected")) {
                avatarSelected = true;
                selectedAvatarID = avatar.querySelector("img").dataset.id;
            }
        }

        if (avatarSelected) {
            fetch("/account/change_avatar/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "id": selectedAvatarID
                }),
                mode: "same-origin"
            })
                .then(response => {
                    if (response.ok) {
                        return response.json()
                    } else {
                        throw new Error(response.statusText)
                    }
                })
                .then(response => {
                    updateAvatar(response.url);
                })
                .catch((error) => console.log(error.message))
        } else {
            console.log("Select avatar");
        }
    })
};
