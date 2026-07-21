const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");
const menuIcon = menuToggle.querySelector("i");

menuToggle.addEventListener("click", function () {
    navLinks.classList.toggle("active");

    const menuIsOpen = navLinks.classList.contains("active");

    menuToggle.setAttribute("aria-expanded", menuIsOpen);

    if (menuIsOpen) {
        menuIcon.classList.remove("fa-bars");
        menuIcon.classList.add("fa-xmark");
    } else {
        menuIcon.classList.remove("fa-xmark");
        menuIcon.classList.add("fa-bars");
    }
});