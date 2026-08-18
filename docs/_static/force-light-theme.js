(function () {
  function forceLightTheme() {
    document.body.dataset.theme = "light";

    try {
      localStorage.setItem("theme", "light");
    } catch (_error) {
      // Ignore storage failures in restricted browsing contexts.
    }
  }

  forceLightTheme();

  const observer = new MutationObserver(() => {
    if (document.body.dataset.theme !== "light") {
      forceLightTheme();
    }
  });

  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
})();
