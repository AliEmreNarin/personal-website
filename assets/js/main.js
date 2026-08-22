(function () {
  var root = document.documentElement;

  // ---- theme toggle -------------------------------------------------------
  var toggle = document.getElementById("theme-toggle");
  function setTheme(t) {
    root.setAttribute("data-theme", t);
    try {
      localStorage.setItem("theme", t);
    } catch (e) {}
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }

  // ---- tabs (library present/past) ---------------------------------------
  document.querySelectorAll("[data-tabs]").forEach(function (tabs) {
    var buttons = tabs.querySelectorAll("[data-tab]");
    var scope = document;
    function activate(name, push) {
      buttons.forEach(function (b) {
        b.setAttribute("aria-selected", b.dataset.tab === name ? "true" : "false");
      });
      scope.querySelectorAll("[data-pane]").forEach(function (p) {
        p.hidden = p.dataset.pane !== name;
      });
      if (push) {
        try {
          history.replaceState(null, "", "#" + name);
        } catch (e) {}
      }
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        activate(b.dataset.tab, true);
      });
    });
    function fromHash() {
      var h = location.hash.replace("#", "");
      return tabs.querySelector('[data-tab="' + h + '"]') ? h : buttons[0] && buttons[0].dataset.tab;
    }
    activate(fromHash(), false);
    window.addEventListener("hashchange", function () {
      activate(fromHash(), false);
    });
  });
})();
