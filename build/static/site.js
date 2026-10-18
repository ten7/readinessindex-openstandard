/* Progressive enhancement only. Every page reads without this file. */
(function () {
  "use strict";

  // An Index 11 address (#air-1.2) lands on the test it became, or on its row in the
  // crosswalk when the test was retired. Links to the old document are in inboxes.
  function legacy() {
    if (!location.hash) return;
    var hash = decodeURIComponent(location.hash.slice(1));
    // The standard was first published inside a product site, which addressed a test as
    // #c-RCH-1 or #row-RCH-1 and a category as #d-1. Those links are in reports and emails.
    var m = /^(?:c|row)-(.+)$/i.exec(hash);
    if (m) { location.replace("#" + m[1].toLowerCase()); return; }
    m = /^d-(\d+)$/.exec(hash);
    if (m) { location.replace("#d" + m[1]); return; }
    var node = document.getElementById("legacy-map");
    if (!node) return;
    var map;
    try { map = JSON.parse(node.textContent); } catch (e) { return; }
    var target = map[hash.toLowerCase()];
    if (target) location.replace(target);
  }
  legacy();
  window.addEventListener("hashchange", legacy);

  // The contents rail follows the reader.
  var links = Array.prototype.slice.call(document.querySelectorAll(".rail a[href^='#']"));
  if (links.length && "IntersectionObserver" in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var current = null;
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var a = byId[entry.target.id];
        if (!a || a === current) return;
        if (current) current.classList.remove("is-active");
        a.classList.add("is-active");
        current = a;
      });
    }, { rootMargin: "0px 0px -75% 0px" });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) seen.observe(el);
    });
  }

  // A thin reading-progress line on the long page.
  var bar = document.querySelector("[data-progress]");
  if (bar) {
    var fill = bar.firstElementChild;
    var tick = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      fill.style.width = (max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0) + "%";
    };
    window.addEventListener("scroll", tick, { passive: true });
    tick();
  }

  // Filtering the tests.
  var tools = document.querySelector("[data-filter]");
  if (tools) {
    var rows = Array.prototype.slice.call(document.querySelectorAll(".test"));
    var groups = Array.prototype.slice.call(document.querySelectorAll(".group"));
    var q = tools.querySelector("[name=q]");
    var ev = tools.querySelector("[name=evidence]");
    var scope = tools.querySelector("[name=scope]");
    var out = tools.querySelector("output");
    var apply = function () {
      var text = q.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (row) {
        var ok = (!text || row.getAttribute("data-search").indexOf(text) !== -1) &&
          (!ev.value || row.getAttribute("data-evidence") === ev.value) &&
          (!scope.value || row.getAttribute("data-scored") === scope.value);
        row.hidden = !ok;
        if (ok) shown += 1;
      });
      groups.forEach(function (g) {
        g.hidden = !g.querySelector(".test:not([hidden])");
      });
      out.textContent = shown + " of " + rows.length + " tests";
    };
    [q, ev, scope].forEach(function (el) { el.addEventListener("input", apply); });
    apply();
    // Opening a test from a link opens its detail too.
    var open = function () {
      var id = location.hash.slice(1);
      var row = id && document.getElementById(id);
      if (row && row.classList.contains("test")) {
        row.hidden = false;
        var d = row.querySelector("details");
        if (d) d.open = true;
      }
    };
    open();
    window.addEventListener("hashchange", open);
  }
})();
