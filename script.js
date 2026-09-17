// ==========================================
// FREELEARN HUB - JAVASCRIPT
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ------------------------------------------
    // SEARCH COURSES
    // ------------------------------------------

    const searchInput = document.getElementById("searchInput");
    const courseCards = document.querySelectorAll(".course-card");

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const searchText = searchInput.value.toLowerCase().trim();

            courseCards.forEach(function (card) {

                const courseText = card.innerText.toLowerCase();

                if (courseText.includes(searchText)) {
                    card.style.display = "";
                } else {
                    card.style.display = "none";
                }

            });

        });

    }


    // ------------------------------------------
    // SEARCH BUTTON
    // ------------------------------------------

    const searchButton = document.getElementById("searchButton");

    if (searchButton && searchInput) {

        searchButton.addEventListener("click", function () {

            const searchText = searchInput.value.toLowerCase().trim();

            courseCards.forEach(function (card) {

                const courseText = card.innerText.toLowerCase();

                if (courseText.includes(searchText)) {
                    card.style.display = "";
                } else {
                    card.style.display = "none";
                }

            });

        });

    }


    // ------------------------------------------
    // CLEAR SEARCH
    // ------------------------------------------

    const clearButton = document.getElementById("clearSearch");

    if (clearButton && searchInput) {

        clearButton.addEventListener("click", function () {

            searchInput.value = "";

            courseCards.forEach(function (card) {
                card.style.display = "";
            });

        });

    }


    // ------------------------------------------
    // CONFIRM BEFORE OPENING COURSE
    // ------------------------------------------

    const courseLinks = document.querySelectorAll(".course-link");

    courseLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            const courseName = link.dataset.course;

            if (courseName) {

                const confirmOpen = confirm(
                    "Open this course on the provider website?"
                );

                if (!confirmOpen) {
                    event.preventDefault();
                }

            }

        });

    });


    // ------------------------------------------
    // MOBILE MENU
    // ------------------------------------------

    const menuButton = document.getElementById("menuButton");
    const navLinks = document.getElementById("navLinks");

    if (menuButton && navLinks) {

        menuButton.addEventListener("click", function () {

            navLinks.classList.toggle("show");

        });

    }


    // ------------------------------------------
    // AUTO HIDE ALERT MESSAGE
    // ------------------------------------------

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.opacity = "0";

            setTimeout(function () {
                alert.style.display = "none";
            }, 500);

        }, 4000);

    });

});