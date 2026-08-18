/* The format map. Every list on this page is rendered from data/format.json,
   which the build reads out of the validator's own constants, the spec's own
   headings, and the demo page the walkthrough builds. */
(function () {
  "use strict";

  var fmt = window.__ERGO_FORMAT__;
  var meta = window.__ERGO_META__;
  var kit = window.ergosite;
  if (!fmt || !kit) return;

  var el = kit.el;

  // Counts stated in prose come from the data, never from a writer's memory:
  // blocks and commands have both changed under this page before.
  var WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
               "eight", "nine", "ten", "eleven", "twelve"];
  function spell(n) { return WORDS[n] || String(n); }
  function fill(name, value) {
    document.querySelectorAll('[data-fact="' + name + '"]').forEach(function (node) {
      node.textContent = value;
    });
  }
  fill("block-count", spell((fmt.blocks || []).length));
  fill("command-count", spell((fmt.surface || fmt.commands || []).length));
  fill("lifecycle-count", spell((fmt.lifecycle || []).length));

  // -- the blocks, as a selectable list --------------------------------------
  var nav = document.getElementById("anatomy");
  var detail = document.getElementById("block-detail");

  function keylist(keys, required) {
    var list = el("ul", "keylist");
    keys.forEach(function (key) {
      list.appendChild(el("li", required ? "is-required" : null, key));
    });
    return list;
  }

  function showBlock(block) {
    detail.textContent = "";

    var head = el("div", "block-detail__head");
    head.appendChild(el("h3", null, block.label));
    var badge = el("span", "badge", "[" + block.table + "]");
    head.appendChild(badge);
    if (block.one_per_page) {
      head.appendChild(el("span", "badge", "one per page"));
    }
    var link = el("a", "spec-link", kit.specLabel(block.spec, fmt.sections));
    link.href = kit.specHref(block.spec, fmt.sections);
    head.appendChild(link);
    detail.appendChild(head);

    detail.appendChild(el("p", null, block.summary));

    detail.appendChild(el("p", "pane-label", "Required — the validator errors without these"));
    detail.appendChild(keylist(block.required, true));

    detail.appendChild(el("p", "pane-label", "Optional"));
    detail.appendChild(keylist(block.optional, false));

    detail.appendChild(kit.record({
      path: "docs/data/ridgeway-311.md",
      label: "· real block from the walkthrough's page",
      text: block.example,
      caption: "The block carries the facts. The prose under it carries the story, the "
        + "examples and the numbers — never both."
    }));

    Array.prototype.forEach.call(nav.querySelectorAll("button"), function (button) {
      button.setAttribute("aria-current", String(button.dataset.table === block.table));
    });
  }

  if (nav && detail) {
    var list = el("ul");
    var header = el("li");
    header.appendChild(el("div", "plain", "docs/data/<slug>.md"));
    list.appendChild(header);
    fmt.blocks.forEach(function (block) {
      var item = el("li");
      var button = el("button");
      button.type = "button";
      button.dataset.table = block.table;
      button.appendChild(document.createTextNode("[" + block.table + "]"));
      button.appendChild(el("span", "comment", "  " + block.label.toLowerCase()));
      button.addEventListener("click", function () { showBlock(block); });
      item.appendChild(button);
      list.appendChild(item);
    });
    var footer = el("li");
    footer.appendChild(el("div", "plain", "…prose between the blocks"));
    list.appendChild(footer);
    nav.appendChild(list);
    showBlock(fmt.blocks[0]);
  }

  // -- the vocabularies -----------------------------------------------------
  var vocabHost = document.getElementById("vocabularies");
  if (vocabHost) {
    fmt.vocabularies.forEach(function (vocab) {
      var card = el("div", "vocab");
      var head = el("div", "vocab__head");
      head.appendChild(el("span", "vocab__field", "[" + vocab.table + "] " + vocab.field));
      head.appendChild(el("span", "badge" + (vocab.closed ? " badge--accent" : ""),
        vocab.closed ? "closed" : "recommended"));
      head.appendChild(el("span", "vocab__q", vocab.question));
      var link = el("a", "spec-link", kit.specLabel(vocab.spec, fmt.sections));
      link.href = kit.specHref(vocab.spec, fmt.sections);
      head.appendChild(link);
      card.appendChild(head);

      var values = el("ul", "vocab__values");
      vocab.values.forEach(function (value) {
        var item = document.createElement("li");
        // The effect scale is the one place colour carries meaning; reuse it
        // here rather than inventing a second key for the same four words.
        if (vocab.field === "effect") {
          item.appendChild(kit.chip("effect", value));
        } else {
          item.textContent = value;
        }
        values.appendChild(item);
      });
      card.appendChild(values);
      vocabHost.appendChild(card);
    });
  }

  // -- the lifecycle rail ---------------------------------------------------
  var rail = document.getElementById("rail");
  if (rail) {
    fmt.lifecycle.forEach(function (stage, index) {
      var cell = el("div", "rail__stage");
      // The two stages the validator actually gates on get the accent rule.
      cell.setAttribute("data-gate", index === 1 || index === 3 ? "yes" : "no");
      cell.appendChild(el("div", "rail__name", stage.stage));
      var act = el("code", "rail__act", stage.act);
      cell.appendChild(act);
      cell.appendChild(el("p", null, stage.gains));
      var worth = el("p", "rail__worth", stage.worth);
      cell.appendChild(worth);
      var link = el("a", "spec-link", "SPEC §" + stage.spec);
      link.href = kit.specHref(stage.spec, fmt.sections);
      cell.appendChild(link);
      rail.appendChild(cell);
    });
  }

  // -- conformance ----------------------------------------------------------
  var conf = document.getElementById("conformance");
  if (conf) {
    [
      ["Core — what makes a valid page", fmt.conformance.core, "conformance__core"],
      ["Supplemental — adopt in any order", fmt.conformance.supplemental, "conformance__supp"]
    ].forEach(function (pair) {
      var cell = el("div", pair[2]);
      cell.appendChild(el("h3", null, pair[0]));
      var list = el("ul");
      pair[1].forEach(function (line) {
        var item = document.createElement("li");
        item.appendChild(kit.codeify(line));
        list.appendChild(item);
      });
      cell.appendChild(list);
      conf.appendChild(cell);
    });
  }

  // -- the CLI surface ------------------------------------------------------
  var cli = document.getElementById("cli");
  if (cli && meta && meta.cli) {
    var body = document.createElement("tbody");
    meta.cli.forEach(function (command) {
      var row = document.createElement("tr");
      row.appendChild(el("td", null, command.name));
      var cell = el("td", null, command.summary);
      if (command.usage) cell.appendChild(el("code", "usage", command.usage));
      row.appendChild(cell);
      body.appendChild(row);
    });
    cli.appendChild(body);
  }
})();
