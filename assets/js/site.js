"use strict";

const navigation = document.querySelector(".navigation");
const menuToggle = document.querySelector(".menu-toggle");
if (navigation && menuToggle) {
  navigation.classList.add("enhanced");
  menuToggle.hidden = false;
  const closeMenu = () => {
    navigation.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
  };
  menuToggle.addEventListener("click", () => {
    const opened = navigation.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", String(opened));
  });
  navigation.querySelectorAll(".nav-links a").forEach(link => link.addEventListener("click", closeMenu));
  navigation.addEventListener("keydown", event => {
    if (event.key === "Escape" && navigation.classList.contains("is-open")) {
      closeMenu();
      menuToggle.focus();
    }
  });
  window.matchMedia("(min-width: 901px)").addEventListener("change", closeMenu);
}

const carousel = document.querySelector(".carousel");
if (carousel) {
  const track = carousel.querySelector(".carousel-track");
  const slides = Array.from(carousel.querySelectorAll(".slide"));
  const dots = Array.from(carousel.querySelectorAll(".carousel-dot"));
  const status = carousel.querySelector(".slide-status");
  const controls = carousel.querySelector(".carousel-controls");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let current = 0;
  let scrollFrame = 0;

  const update = index => {
    current = index;
    dots.forEach((dot, number) => {
      if (number === index) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });
    const caption = slides[index].querySelector("figcaption").textContent;
    status.textContent = `${index + 1} / ${slides.length} · ${caption}`;
  };
  const show = (index, animate = true) => {
    const next = (index + slides.length) % slides.length;
    update(next);
    track.scrollTo({
      left: next * track.clientWidth,
      behavior: animate && !reducedMotion.matches ? "smooth" : "instant"
    });
  };
  carousel.querySelectorAll("[data-direction]").forEach(button => {
    button.addEventListener("click", () => show(current + Number(button.dataset.direction)));
  });
  dots.forEach((dot, index) => dot.addEventListener("click", () => show(index)));
  track.addEventListener("keydown", event => {
    if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
      event.preventDefault();
      show(current + (event.key === "ArrowRight" ? 1 : -1));
    }
  });
  track.addEventListener("scroll", () => {
    cancelAnimationFrame(scrollFrame);
    scrollFrame = requestAnimationFrame(() => {
      const nearest = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth)));
      if (nearest !== current) update(nearest);
    });
  }, { passive: true });
  const observer = new ResizeObserver(() => show(current, false));
  observer.observe(track);
  carousel.classList.add("enhanced");
  controls.hidden = false;
}
// Keep the same section when changing language; the links also work without JS.
const languageLinks = document.querySelectorAll("[data-language-switch]");
const syncLanguageSections = () => {
  languageLinks.forEach(link => {
    link.hash = window.location.hash;
  });
};
syncLanguageSections();
window.addEventListener("hashchange", syncLanguageSections);