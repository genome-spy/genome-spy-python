/* Native scrolling keeps the example groups usable without JavaScript, too. */
(function () {
  function setupShowcase() {
    const viewport = document.querySelector(".gs-showcase-pages");
    if (!viewport) return;
    const pages = [...viewport.children];
    const controls = document.querySelector(".gs-showcase-controls");
    const status = controls.querySelector(".gs-showcase-status");
    let current = 0;
    const ellipsis = () => {
      const span = document.createElement("span");
      span.className = "gs-showcase-ellipsis";
      span.textContent = "···";
      span.setAttribute("aria-hidden", "true");
      return span;
    };
    const before = ellipsis();
    const after = ellipsis();
    controls.append(before);
    // Keep buttons in the DOM so the moving window does not recreate focus.
    const buttons = pages.map((page, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.setAttribute("aria-label", `Show gallery page ${index + 1} of ${pages.length}`);
      button.setAttribute("aria-controls", viewport.id);
      button.addEventListener("click", () => goTo(index));
      controls.append(button);
      return button;
    });
    controls.append(after);

    function pageWidth() {
      return pages.length > 1
        ? pages[1].offsetLeft - pages[0].offsetLeft
        : pages[0].getBoundingClientRect().width;
    }

    function update() {
      current = Math.max(0, Math.min(pages.length - 1, Math.round(viewport.scrollLeft / pageWidth())));
      const start = Math.max(0, Math.min(current - 2, pages.length - 5));
      const end = Math.min(start + 5, pages.length);
      const focused = document.activeElement;
      buttons.forEach((button, index) => {
        button.hidden = index < start || index >= end;
        if (index === current) button.setAttribute("aria-current", "page");
        else button.removeAttribute("aria-current");
      });
      before.style.visibility = start > 0 ? "visible" : "hidden";
      after.style.visibility = end < pages.length ? "visible" : "hidden";
      if (buttons.includes(focused) && focused.hidden) buttons[current].focus({ preventScroll: true });
      const label = `Gallery page ${current + 1} of ${pages.length}`;
      if (status.textContent !== label) status.textContent = label;
    }

    function goTo(index) {
      index = Math.max(0, Math.min(pages.length - 1, index));
      viewport.scrollTo({
        left: index * pageWidth(),
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth",
      });
    }

    viewport.addEventListener("scroll", update, { passive: true });
    function onKeyDown(event) {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      const index = event.key === "Home" ? 0 : event.key === "End" ? pages.length - 1
        : current + (event.key === "ArrowRight" ? 1 : -1);
      goTo(index);
    }
    viewport.addEventListener("keydown", (event) => {
      if (event.target === viewport) onKeyDown(event);
    });
    controls.addEventListener("keydown", onKeyDown);
    window.addEventListener("resize", update);
    controls.hidden = pages.length < 2;
    update();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupShowcase);
  } else {
    setupShowcase();
  }
})();
