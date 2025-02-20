$(document).ready(function () {
    // Create a top loading bar
    const loader = $('<div id="loader" style="position: fixed; top: 0; left: 0; height: 4px; width: 0; background: green; z-index: 9999; transition: width 0.3s;"></div>');
    $('body').append(loader);

    $("a").on("click", (e) => {
        const url = e.currentTarget.href;

        // Ignore anchor links
        if (url.includes("#")) return;

        e.preventDefault();

        const content = $("#content");
        loader.css("width", "50%").show(); // Reset and show loader

        $.get(url, (data) => {
            loader.css("width", "100%"); // Fill loader
            content.html(data); // Update content
            history.pushState(null, null, url); // Update history
            setTimeout(() => {
                content.css("opacity", 0);
            }, 100);
            setTimeout(() => {
                content.css("opacity", 1);
            }, 150);
            setTimeout(() => {
                loader.hide(); // Hide loader
            }, 350);
        }).fail(() => {
            loader.css("width", "0").hide(); // Reset loader on failure
            alert("Failed to load page");
        });
    });

    window.onpopstate = function () {
        const url = location.href; // Use full URL

        // Ignore anchor links
        if (url.includes("#")) return;

        loader.css("width", "0").show(); // Reset and show loader

        $.get(url, function (data) {
            loader.css("width", "100%");
            $("#content").html(data); // Update content
            setTimeout(() => {
                loader.hide(); // Hide loader
            }, 400);
        }).fail(() => {
            loader.css("width", "0").hide();
            console.error("Failed to load page");
        });
    };

    // Toggle 'scrolled' class on logo when scrolling
    window.addEventListener("scroll", () => {
        const logo = document.querySelector(".logo");
        if (window.scrollY > 100) {
            logo.classList.add("scrolled");
        } else {
            logo.classList.remove("scrolled");
        }
    });
});
