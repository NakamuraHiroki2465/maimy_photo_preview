(() => {
  const root = document.documentElement;
  root.classList.add("js");
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // header: スクロールで背景を付ける
  const header = document.querySelector("[data-header]");
  const onScroll = () => header.classList.toggle("is-scrolled", scrollY > 24);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // mobile drawer
  const toggle = document.querySelector("[data-menu-toggle]");
  const drawer = document.querySelector("[data-drawer]");
  const setMenu = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    drawer.hidden = !open;
    header.classList.toggle("is-solid", open);
    document.body.style.overflow = open ? "hidden" : "";
  };
  toggle.addEventListener("click", () => setMenu(drawer.hidden));
  addEventListener("keydown", (e) => { if (e.key === "Escape" && !drawer.hidden) setMenu(false); });
  matchMedia("(min-width: 1024px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });

  // reveal on scroll
  const targets = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach((el) => io.observe(el));
  } else {
    targets.forEach((el) => el.classList.add("is-visible"));
  }

  // hero slideshow
  const slides = document.querySelectorAll("[data-slideshow] .hero__slide");
  if (slides.length > 1 && !reduceMotion) {
    let i = 0;
    setInterval(() => {
      slides[i].classList.remove("is-active");
      i = (i + 1) % slides.length;
      slides[i].classList.add("is-active");
    }, 6000);
  }

  // gallery filter
  const filterButtons = document.querySelectorAll("[data-filter]");
  const items = document.querySelectorAll("[data-masonry] > li");
  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const cat = btn.dataset.filter;
      filterButtons.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      items.forEach((li) => { li.hidden = cat !== "all" && li.dataset.cat !== cat; });
    });
  });

  // lightbox
  const dialog = document.querySelector("[data-lightbox-dialog]");
  if (dialog && typeof dialog.showModal === "function") {
    const dialogImg = dialog.querySelector("img");
    document.querySelectorAll("[data-lightbox]").forEach((btn) => {
      btn.addEventListener("click", () => {
        dialogImg.src = btn.dataset.lightbox;
        dialogImg.alt = btn.querySelector("img").alt;
        dialog.showModal();
      });
    });
    dialog.addEventListener("click", () => dialog.close());
  }
})();
