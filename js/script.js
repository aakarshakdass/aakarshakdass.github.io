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