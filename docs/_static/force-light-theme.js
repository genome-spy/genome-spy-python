(function () {
  const root = document.documentElement;

  function forceLightTheme() {
    root.dataset.theme = "light";
    root.dataset.mode = "light";

    try {
      localStorage.setItem("theme", "light");
      localStorage.setItem("mode", "light");
      localStorage.setItem("pydata-theme", "light");
    } catch (_error) {
      // Ignore storage failures in restricted browsing contexts.
    }
  }

  forceLightTheme();

  const observer = new MutationObserver(() => {
    if (root.dataset.theme !== "light" || root.dataset.mode !== "light") {
      forceLightTheme();
    }
  });

  observer.observe(root, {
    attributes: true,
    attributeFilter: ["data-theme", "data-mode"],
  });
})();
