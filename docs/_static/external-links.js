(function () {
  function openExternalLinksInNewTabs() {
    for (const link of document.querySelectorAll("a[href]")) {
      const url = new URL(link.href, window.location.href);
      if (url.origin === window.location.origin) {
        continue;
      }
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", openExternalLinksInNewTabs);
  } else {
    openExternalLinksInNewTabs();
  }
})();
