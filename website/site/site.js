/* ergo site — shared behaviour. No dependencies, file:// safe.

   Everything here is progressive enhancement over markup that already works:
   copy buttons appear only if the clipboard API exists, and the data-driven
   records replace a static fallback only once the generated data has loaded. */
(function () {
  "use strict";

  var SPEC_URL = "https://github.com/lavallee/ergo/blob/main/SPEC.md";

  // -- copy buttons on command lines ---------------------------------------
  // Added by script so a reader without clipboard support never sees a control
  // that cannot do anything. Idempotent, so pages that swap in new command
  // lines can call it again.
  function enhance() {
    if (!navigator.clipboard || window.isSecureContext === false) return;
    document.querySelectorAll(".cmd").forEach(function (cmd) {
      if (cmd.querySelector(".copy")) return;
      var code = cmd.querySelector("code");
      if (!code) return;
      var button = document.createElement("button");
      button.type = "button";
      button.className = "copy";
      button.textContent = "copy";
      button.setAttribute("aria-label", "Copy command: " + code.textContent);
      button.addEventListener("click", function () {
        navigator.clipboard.writeText(code.textContent).then(function () {
          button.textContent = "copied";
          button.setAttribute("data-copied", "yes");
          window.setTimeout(function () {
            button.textContent = "copy";
            button.removeAttribute("data-copied");
          }, 1600);
        }, function () {
          button.textContent = "press ⌘C";
        });
      });
      cmd.appendChild(button);
    });
  }

  enhance();

  window.ergosite = {
    /** Attach copy buttons to any command lines added since the last call. */
    enhance: enhance,

    /** Create an element with an optional class and text. */
    el: function (tag, cls, text) {
      var node = document.createElement(tag);
      if (cls) node.className = cls;
      if (text != null) node.textContent = text;
      return node;
    },

    /** Render `backticked` spans and [markdown](links) found in page prose.
     *
     * The prose on this site is sliced out of real markdown files, so it
     * arrives with markdown inline syntax in it. Only these two forms are
     * handled — anything else is shown as written rather than half-rendered.
     */
    codeify: function (text) {
      var fragment = document.createDocumentFragment();
      var pattern = /`([^`]+)`|\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g;
      var last = 0;
      var match;
      while ((match = pattern.exec(text))) {
        if (match.index > last) {
          fragment.appendChild(document.createTextNode(text.slice(last, match.index)));
        }
        if (match[1] !== undefined) {
          var code = document.createElement("code");
          code.textContent = match[1];
          fragment.appendChild(code);
        } else {
          var link = document.createElement("a");
          link.href = match[3];
          link.textContent = match[2];
          fragment.appendChild(link);
        }
        last = match.index + match[0].length;
      }
      fragment.appendChild(document.createTextNode(text.slice(last)));
      return fragment;
    },

    /** Build the standard record block: chip, literal content, caption. */
    record: function (options) {
      var wrap = document.createElement("div");
      wrap.className = "record" + (options.refused ? " record--refused" : "");

      var chip = document.createElement("div");
      chip.className = "record__chip";
      var path = document.createElement("strong");
      path.textContent = options.path || "";
      chip.appendChild(path);
      if (options.label) chip.appendChild(document.createTextNode(options.label));
      if (options.truncated) {
        var more = document.createElement("span");
        more.textContent = "· truncated";
        chip.appendChild(more);
      }
      wrap.appendChild(chip);

      var pre = document.createElement("pre");
      var code = document.createElement("code");
      code.textContent = options.text || "";
      pre.appendChild(code);
      wrap.appendChild(pre);

      if (options.caption) {
        var caption = document.createElement("p");
        caption.className = "record__caption";
        caption.textContent = options.caption;
        wrap.appendChild(caption);
      }
      return wrap;
    },

    /** An effect / status / core chip, using the one colour scale the site has. */
    chip: function (kind, value) {
      var node = document.createElement("span");
      if (kind === "core") {
        node.className = "eff eff--core";
        node.textContent = "core";
        node.title = "Read before any contact with the dataset, whatever the slice";
        return node;
      }
      node.className = kind === "status" ? "eff eff--status" : "eff";
      node.setAttribute("data-" + kind, value);
      node.textContent = value;
      return node;
    },

    /** Link into the spec at a numbered section. */
    specHref: function (number, sections) {
      var match = (sections || []).filter(function (s) { return s.number === String(number); })[0];
      return match ? SPEC_URL + "#" + match.anchor : SPEC_URL;
    },

    specLabel: function (number, sections) {
      var match = (sections || []).filter(function (s) { return s.number === String(number); })[0];
      return match ? "SPEC §" + match.number + " " + match.title.replace(/`/g, "") : "SPEC";
    }
  };
})();
