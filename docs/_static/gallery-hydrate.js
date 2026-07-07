/*
 * Detail-page embeds: mount a live, interactive GenomeSpy chart when the
 * placeholder scrolls into view. Gallery and showcase tiles are static images
 * and need no JavaScript.
 *
 * The GenomeSpy `embed` entrypoint is imported lazily from the pinned
 * @genome-spy/core CDN bundle recorded on the element's data-bundle attribute.
 */
(function () {
  "use strict";

  const bundleCache = new Map();

  function loadEmbed(url) {
    if (!bundleCache.has(url)) {
      bundleCache.set(
        url,
        import(url).then(function (mod) {
          const embed = mod.embed || (mod.default && mod.default.embed) || mod.default;
          if (typeof embed !== "function") {
            throw new Error("GenomeSpy embed export was not found.");
          }
          return embed;
        })
      );
    }
    return bundleCache.get(url);
  }

  async function mount(host) {
    if (host.dataset.mounted) return;
    host.dataset.mounted = "1";
    host.classList.add("is-loading");
    try {
      const [embed, spec] = await Promise.all([
        loadEmbed(host.dataset.bundle),
        fetch(host.dataset.spec).then(function (r) {
          if (!r.ok) throw new Error("Failed to load spec: " + host.dataset.spec);
          return r.json();
        }),
      ]);
      host.classList.remove("is-loading");
      await embed(host, spec, {});
      host.classList.add("is-live");
    } catch (err) {
      host.dataset.mounted = "";
      host.classList.remove("is-loading");
      host.classList.add("is-error");
      host.textContent = "Could not render this chart. See the browser console for details.";
      console.error(err);
    }
  }

  function init() {
    const hosts = document.querySelectorAll(".gs-live-embed[data-autoload]");
    if (!hosts.length) return;
    const io = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            mount(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "200px" }
    );
    hosts.forEach(function (host) {
      io.observe(host);
    });
  }

  if (document.readyState !== "loading") {
    init();
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
