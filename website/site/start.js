/* Start page: one generated record, so the reader sees what `digest` really
   emits rather than a sample of what it might emit. Everything else on the page
   is a command you can paste — deliberately no invented output beside it. */
(function () {
  "use strict";

  var walk = window.__ERGO_WALK__;
  var kit = window.ergosite;
  if (!walk || !kit) return;

  var step = (walk.steps || []).filter(function (s) { return s.id === "digest"; })[0];
  var host = document.getElementById("start-index");
  if (!step || !host) return;

  host.appendChild(kit.record({
    path: step.record.path,
    label: "· generated for the walkthrough's page",
    text: step.record.text,
    caption: step.record.caption
  }));
})();
