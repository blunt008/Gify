const avatar = document.getElementById("avatar");
const popoverProfile = document.getElementById("popover-profile");
const avatarLink = document.getElementById("avatar-link");

$(avatar).popover({
  trigger: 'focus',
    container: avatarLink,
    html: true,
    boundary: "viewport",
    content: function() {
        return $(popoverProfile).html();
    },
})

avatar.addEventListener("click", (event) => {
    event.preventDefault();
})

