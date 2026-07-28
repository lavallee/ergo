/* The example page, rendered from data/example.json — which is what
   `ergo.py export examples/spr.md` emitted at build time, plus each entry's
   prose sliced out of the same markdown file. Nothing on this page is retyped
   from the source; if a field disappears from the format, it disappears here. */
(function () {
  "use strict";

  var page = window.__ERGO_PAGE__;
  var kit = window.ergosite;
  if (!page || !kit) return;

  var el = kit.el;
  var d = page.dataset || {};

  // -- masthead and manifest ------------------------------------------------
  var title = document.getElementById("pg-title");
  if (title) title.textContent = d.title || "The example data page";

  var lede = document.getElementById("pg-lede");
  if (lede && page.lede) {
    lede.textContent = "";
    lede.appendChild(kit.codeify(page.lede.replace(/\n/g, " ")));
  }

  function fact(term, value, note) {
    if (!value) return null;
    var cell = el("div", "fact");
    cell.appendChild(el("dt", null, term));
    var dd = el("dd", null, value);
    dd.style.fontSize = "var(--text-base)";
    if (note) dd.appendChild(el("small", null, note));
    cell.appendChild(dd);
    return cell;
  }

  var manifest = document.getElementById("pg-manifest");
  if (manifest) {
    var coverage = d.coverage || {};
    var missing = d.missingness || {};
    [
      fact("Publisher", d.publisher),
      fact("Status", d.status, d.version || ""),
      fact("Source confidence", d.confidence, "A authoritative primary · B official document · C secondary · ? unjudged"),
      fact("Updated", d.updated, "last substantive page edit"),
      fact("Coverage", coverage.years, coverage.grain || ""),
      fact("Entities", coverage.entities),
      fact("Zero means missing", missing.zero_is_missing === true ? "yes" : (missing.zero_is_missing === false ? "no" : ""),
        (missing.source_tokens || []).length ? "also: " + missing.source_tokens.join(" · ") : ""),
      fact("Subject", (d.subject || "").replace(/^https?:\/\//, ""), "the identity claim a directory clusters on")
    ].forEach(function (cell) {
      if (cell) manifest.appendChild(cell);
    });
  }

  var pitfall = document.getElementById("pg-pitfall");
  if (pitfall && d.pitfall) {
    pitfall.appendChild(el("p", "pane-label", "The pitfall — required, and the line that travels"));
    pitfall.appendChild(el("p", null, d.pitfall));
  }

  var unknowns = document.getElementById("pg-unknowns");
  if (unknowns && (d.unknowns || []).length) {
    unknowns.appendChild(el("p", "pane-label", "Where this page's knowledge stops"));
    var list = document.createElement("ul");
    d.unknowns.forEach(function (line) {
      var item = document.createElement("li");
      item.style.fontSize = "var(--text-sm)";
      item.style.color = "var(--text-2)";
      item.textContent = line;
      list.appendChild(item);
    });
    unknowns.appendChild(list);
  }

  // -- entries --------------------------------------------------------------
  function proseFor(id) {
    var text = (page.prose || {})[id];
    if (!text) return null;
    var wrap = el("div", "entry__prose");
    text.split(/\n\s*\n/).forEach(function (para) {
      var p = document.createElement("p");
      p.appendChild(kit.codeify(para.replace(/\n/g, " ").trim()));
      wrap.appendChild(p);
    });
    return wrap;
  }

  function field(label, value, modifier) {
    if (!value) return null;
    var p = el("p", "entry__field" + (modifier ? " entry__field--" + modifier : ""));
    p.appendChild(el("span", "k", label));
    p.appendChild(document.createTextNode(" " + value));
    return p;
  }

  function scopeLine(scope) {
    if (!scope) return null;
    var parts = [];
    Object.keys(scope).forEach(function (key) {
      var value = scope[key];
      if (value === true) parts.push(key + " = true");
      else if (Array.isArray(value)) parts.push(key + " = [" + value.join(", ") + "]");
      else parts.push(key + " = " + value);
    });
    if (!parts.length) return null;
    var node = el("div", "entry__scope", "[scope] " + parts.join("  ·  "));
    return node;
  }

  function renderIssue(issue) {
    var entry = el("article", "entry");
    entry.id = "issue-" + issue.id;
    entry.setAttribute("data-effect", issue.effect || "");
    entry.setAttribute("data-kind", "issue");

    var head = el("div", "entry__head");
    head.appendChild(el("span", "entry__id", issue.id));
    head.appendChild(el("h3", "entry__title", issue.title));
    var chips = el("div", "entry__chips");
    if (issue.core === true) chips.appendChild(kit.chip("core"));
    chips.appendChild(kit.chip("effect", issue.effect));
    chips.appendChild(kit.chip("status", issue.status));
    chips.appendChild(el("span", "eff", issue.type));
    head.appendChild(chips);
    entry.appendChild(head);

    [
      field("misuse", issue.misuse, "misuse"),
      field("instead", issue.instead, "instead"),
      field("detection", issue.detection),
      field("handled by", (issue.handled_by || []).join(" · ")),
      field("discovered", issue.discovered)
    ].forEach(function (node) { if (node) entry.appendChild(node); });

    var scope = scopeLine(issue.scope);
    if (scope) entry.appendChild(scope);

    var prose = proseFor(issue.id);
    if (prose) entry.appendChild(prose);
    return entry;
  }

  function renderPractice(practice) {
    var entry = el("article", "entry");
    entry.id = "practice-" + practice.id;
    entry.setAttribute("data-kind", "practice");

    var head = el("div", "entry__head");
    head.appendChild(el("span", "entry__id", practice.id));
    head.appendChild(el("h3", "entry__title", practice.title));
    var chips = el("div", "entry__chips");
    chips.appendChild(el("span", "eff", practice.authority));
    if (practice.contested === true) {
      var contested = el("span", "eff", "contested");
      contested.setAttribute("data-effect", "misleads");
      chips.appendChild(contested);
    }
    head.appendChild(chips);
    entry.appendChild(head);

    entry.appendChild(field("question", practice.question));
    if (Array.isArray(practice.rule)) {
      var label = el("p", "entry__field");
      label.appendChild(el("span", "k", "rule"));
      entry.appendChild(label);
      var steps = el("ol", "entry__rule");
      practice.rule.forEach(function (line) { steps.appendChild(el("li", null, line)); });
      entry.appendChild(steps);
    } else {
      entry.appendChild(field("rule", practice.rule));
    }

    [
      field("naive", practice.naive),
      field("because", practice.because),
      field("because not", practice.because_not),
      field("stops at", practice.stops_at),
      field("irreversible", practice.irreversible),
      field("residual", practice.residual),
      field("addresses", (practice.addresses || []).join(" · ")),
      field("implemented by", (practice.implemented_by || []).join(" · "))
    ].forEach(function (node) { if (node) entry.appendChild(node); });

    var prose = proseFor(practice.id);
    if (prose) entry.appendChild(prose);
    return entry;
  }

  var issuesHost = document.getElementById("pg-issues");
  var issues = page.issues || [];
  if (issuesHost) {
    issues.forEach(function (issue) { issuesHost.appendChild(renderIssue(issue)); });
  }

  var practicesHost = document.getElementById("pg-practices");
  if (practicesHost) {
    (page.practices || []).forEach(function (practice) {
      practicesHost.appendChild(renderPractice(practice));
    });
  }

  // -- filters --------------------------------------------------------------
  // Only the effects this page actually uses get a button: an empty filter is
  // an invitation to a dead end.
  var filters = document.getElementById("pg-filters");
  if (filters && issues.length) {
    var counts = {};
    issues.forEach(function (issue) {
      counts[issue.effect] = (counts[issue.effect] || 0) + 1;
    });
    var cores = issues.filter(function (i) { return i.core === true; }).length;

    function apply(value) {
      issues.forEach(function (issue) {
        var node = document.getElementById("issue-" + issue.id);
        if (!node) return;
        var show = value === "all"
          || (value === "core" ? issue.core === true : issue.effect === value);
        node.hidden = !show;
      });
      Array.prototype.forEach.call(filters.querySelectorAll("button"), function (button) {
        button.setAttribute("aria-pressed", String(button.dataset.value === value));
      });
    }

    var options = [["all", "all", issues.length]];
    if (cores) options.push(["core", "core", cores]);
    ["breaks", "corrupts", "misleads", "context"].forEach(function (effect) {
      if (counts[effect]) options.push([effect, effect, counts[effect]]);
    });

    options.forEach(function (option) {
      var button = el("button", "pg__filter");
      button.type = "button";
      button.dataset.value = option[0];
      button.appendChild(document.createTextNode(option[1] + " "));
      button.appendChild(el("span", "pg__filter-count", String(option[2])));
      button.addEventListener("click", function () { apply(option[0]); });
      filters.appendChild(button);
    });
    apply("all");
  }

  // -- validation -----------------------------------------------------------
  var validations = document.getElementById("pg-validations");
  var section = document.getElementById("pg-validation-section");
  if (validations && (page.validations || []).length) {
    var head = document.createElement("thead");
    var headRow = document.createElement("tr");
    ["date", "method", "result"].forEach(function (label) {
      var th = document.createElement("th");
      th.scope = "col";
      th.textContent = label;
      headRow.appendChild(th);
    });
    head.appendChild(headRow);
    validations.appendChild(head);

    var body = document.createElement("tbody");
    page.validations.forEach(function (record) {
      var row = document.createElement("tr");
      row.appendChild(el("td", null, record.date));
      row.appendChild(el("td", null, record.method));
      row.appendChild(el("td", null, record.result));
      body.appendChild(row);
    });
    validations.appendChild(body);
  } else if (section) {
    section.hidden = true;
  }

  // -- vintage --------------------------------------------------------------
  var vintage = document.getElementById("pg-vintage");
  if (vintage && page.check) {
    vintage.appendChild(document.createTextNode(" At that revision: " + page.check + "."));
  }
})();
