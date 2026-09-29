"use strict";

/**
 * Light and dark mode
 */

const /**{HTMLElement} */ $themeBtn = document.querySelector("[data-theme-btn]");
const /**{HTMLElement} */ $HTML = document.documentElement;
let /**{Boolean | String} */ isDark = window.matchMedia("(prefers-color-scheme:dark)").matches;

const savedTheme = sessionStorage.getItem("theme");
if (savedTheme) {
    $HTML.dataset.theme = savedTheme;
} else {
    $HTML.dataset.theme = isDark ? "dark" : "light";
    sessionStorage.setItem("theme", $HTML.dataset.theme);
}

const changeTheme = () => {
    const currentTheme = sessionStorage.getItem("theme");
    $HTML.dataset.theme = currentTheme === "light" ? "dark" : "light";
    sessionStorage.setItem("theme", $HTML.dataset.theme);

    // Update the button's aria-label for accessibility
    $themeBtn.setAttribute("aria-label", $HTML.dataset.theme === "light" ? "Switch to dark mode" : "Switch to light mode");
}

$themeBtn.addEventListener("click", changeTheme);

/**
 * Tab
 */

const /**{NodeList} */ $tabBtn = document.querySelectorAll("[data-tab-btn]");
let /** {HTMLElement} */ lastActiveTab = document.querySelector("[data-tab-content]"); // Single element
let /** {HTMLElement} */ lastActiveTabBtn = $tabBtn[0]; // First element

$tabBtn.forEach(item => {
    item.addEventListener("click", function () {
        lastActiveTab.classList.remove("active");
        lastActiveTabBtn.classList.remove("active");

        const /**{HTMLElement} */ $tabContent = document.querySelector(`[data-tab-content="${item.dataset.tabBtn}"]`);
        $tabContent.classList.add("active");
        this.classList.add("active");

        lastActiveTab = $tabContent;
        lastActiveTabBtn = this;
    });
});

/* ===== Carousel (append to the end of js/script.js) ===== */
(function () {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    document.querySelectorAll("[data-carousel]").forEach(function (root) {
        const track = root.querySelector(".carousel-track");
        const slides = Array.from(track.children);
        const prevBtn = root.querySelector("[data-carousel-prev]");
        const nextBtn = root.querySelector("[data-carousel-next]");
        const dotsWrap = root.querySelector(".carousel-dots");
        let current = 0;

        // build scroll markers
        const dots = slides.map(function (_, i) {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.className = "carousel-dot";
            dot.setAttribute("aria-label", "Go to image " + (i + 1));
            dot.addEventListener("click", function () { goTo(i); });
            dotsWrap.appendChild(dot);
            return dot;
        });

        function goTo(index) {
            const count = slides.length;
            current = (index + count) % count; // wraps around at both ends
            track.scrollTo({
                left: current * track.clientWidth,
                behavior: reduceMotion ? "auto" : "smooth"
            });
        }

        function update() {
            const width = track.clientWidth;
            const index = width ? Math.round(track.scrollLeft / width) : current;
            current = index;
            dots.forEach(function (dot, i) {
                dot.classList.toggle("active", i === index);
                dot.setAttribute("aria-current", i === index ? "true" : "false");
            });
        }

        prevBtn.addEventListener("click", function () { goTo(current - 1); });
        nextBtn.addEventListener("click", function () { goTo(current + 1); });

        track.addEventListener("scroll", update, { passive: true });
        track.addEventListener("keydown", function (e) {
            if (e.key === "ArrowLeft") { e.preventDefault(); goTo(current - 1); }
            if (e.key === "ArrowRight") { e.preventDefault(); goTo(current + 1); }
        });
        window.addEventListener("resize", function () {
            track.scrollTo({ left: current * track.clientWidth, behavior: "auto" });
        });

        update();
        dots[0].classList.add("active"); // in case the tab is hidden on load
    });
})();
