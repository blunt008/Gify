const avatar = document.getElementById("avatar-link");
const popoverProfile = document.getElementById("popover-profile");

$(avatar).popover({
  trigger: 'focus',
    container: "body",
    html: true,
    boundary: "viewport",
    content: function() {
        return $(popoverProfile).html();
    },
})

avatar.addEventListener("click", (event) => {
    event.preventDefault();
})

