/* Ruidong Li · shared interactions v2.2 (UTF-8).
   Content, navigation and profile are already present in the HTML. */
(() => {
  "use strict";
  document.documentElement.classList.add("has-js");
  const footer = document.querySelector("#site-footer");
  if (footer) footer.textContent = `\u00a9 ${new Date().getFullYear()} Ruidong Li.`;

  const toggle = document.querySelector(".menu-toggle");
  const primaryNav = document.querySelector(".primary-nav");
  const closeMenu = (restoreFocus = false) => {
    if (!toggle || !primaryNav) return;
    primaryNav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    if (restoreFocus) toggle.focus();
  };
  if (toggle && primaryNav) {
    toggle.addEventListener("click", () => {
      const open = primaryNav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    primaryNav.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => closeMenu());
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && primaryNav.classList.contains("is-open")) closeMenu(true);
    });
    window.matchMedia("(min-width: 901px)").addEventListener("change", event => {
      if (event.matches) closeMenu();
    });
  }

  document.querySelectorAll(".abstract-toggle").forEach(button => {
    const details = document.getElementById(button.getAttribute("aria-controls"));
    if (!(details instanceof HTMLDetailsElement)) return;
    const summary = details.querySelector("summary");
    if (summary) summary.hidden = true;
    button.hidden = false;
    const syncState = () => button.setAttribute("aria-expanded", String(details.open));
    button.addEventListener("click", () => {
      details.open = !details.open;
      syncState();
    });
    details.addEventListener("toggle", syncState);
    syncState();
  });
})();
