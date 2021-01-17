const avatar = document.getElementById("avatar");
const popoverProfile = document.getElementById("popover-profile");

$(avatar).popover({
  trigger: 'focus',
    container: "body",
    html: true,
    content: function() {
        return $(popoverProfile).html();
    },
})

avatar.addEventListener("click", (event) => {
    event.preventDefault();
})

