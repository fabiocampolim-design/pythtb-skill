/* SPDX-License-Identifier: Apache-2.0
   Copyright 2026 Fabio Campolim
   DeckNav for the pythtb-skill course (from the AILECTURE decks; section entries may be objects). */
/* DeckNav — two-row section/subsection navigator (bottom-right).
   Top row jumps SECTION to SECTION (the layman pass: abstract tops of each act).
   Bottom row jumps SUBSECTION to SUBSECTION within the flow (the deep pass).
   Arrow keys / clicker traverse everything (reveal navigationMode: "linear");
   Shift+←/→ jump sections from the keyboard.
   Section display names come from DECK_CONTENT.sections[data-sec]. */
window.DeckNav = (function () {
  "use strict";

  function init(R) {
    var names = (window.DECK_CONTENT && window.DECK_CONTENT.sections) || {};
    var el = document.createElement("div");
    el.className = "deck-nav";
    el.innerHTML =
      '<div class="dn-row dn-sec">' +
      '<button id="dn-sec-prev" title="previous section (Shift+←)">‹</button>' +
      '<span id="dn-sec-label"></span>' +
      '<button id="dn-sec-next" title="next section (Shift+→)">›</button></div>' +
      '<div class="dn-row dn-sub">' +
      '<button id="dn-sub-prev" title="previous subsection">‹</button>' +
      '<span id="dn-sub-label"></span>' +
      '<button id="dn-sub-next" title="next subsection">›</button></div>';
    document.body.appendChild(el);

    function stacks() { return R.getHorizontalSlides(); }
    function stackLen(h) {
      var s = stacks()[h];
      if (!s) return 1;
      var subs = s.querySelectorAll("section");
      return subs.length || 1;
    }
    function secName(h) {
      var s = stacks()[h];
      var key = s && s.getAttribute("data-sec");
      var entry = key && names[key];           // string, or {name: ...} (course content)
      return (entry && (entry.name || entry)) || "";
    }
    function curF() {
      var f = R.getIndices().f;
      return f === undefined ? -1 : f;
    }
    function update() {
      var i = R.getIndices();
      document.getElementById("dn-sec-label").textContent =
        secName(i.h) + "  " + (i.h + 1) + "/" + stacks().length;
      document.getElementById("dn-sub-label").textContent =
        (i.v + 1) + "/" + stackLen(i.h);
      document.getElementById("dn-sec-prev").disabled = i.h === 0;
      document.getElementById("dn-sec-next").disabled = i.h === stacks().length - 1;
      document.getElementById("dn-sub-prev").disabled = i.h === 0 && i.v === 0 && curF() === -1;
      document.getElementById("dn-sub-next").disabled =
        i.h === stacks().length - 1 && i.v === stackLen(i.h) - 1;
    }
    // Slide ENTRY always lands at the start (f = -1): animations restart
    // whenever a subsection is (re)entered, in any direction.
    function secJump(dir) {
      var i = R.getIndices();
      var h = Math.max(0, Math.min(stacks().length - 1, i.h + dir));
      if (h !== i.h) R.slide(h, 0, -1);
    }
    function subNext() {
      var i = R.getIndices();
      if (i.v + 1 < stackLen(i.h)) R.slide(i.h, i.v + 1, -1);
      else if (i.h < stacks().length - 1) R.slide(i.h + 1, 0, -1);
    }
    function subPrev() { // media-player style: restart current first, then go back
      var i = R.getIndices();
      if (curF() > -1) { R.slide(i.h, i.v, -1); return; }
      if (i.v > 0) R.slide(i.h, i.v - 1, -1);
      else if (i.h > 0) R.slide(i.h - 1, stackLen(i.h - 1) - 1, -1);
    }
    function controlFocused(e) {
      var t = e.target;
      return t && t.closest && t.closest(".reveal") &&
        /^(INPUT|SELECT|TEXTAREA|BUTTON)$/.test(t.tagName);
    }
    document.getElementById("dn-sec-prev").addEventListener("click", function () { secJump(-1); });
    document.getElementById("dn-sec-next").addEventListener("click", function () { secJump(1); });
    document.getElementById("dn-sub-prev").addEventListener("click", function () { subPrev(); });
    document.getElementById("dn-sub-next").addEventListener("click", function () { subNext(); });
    document.addEventListener("keydown", function (e) {
      if (controlFocused(e)) return;
      if (R.isOverview && R.isOverview()) return; // overview grid keeps native arrows
      if (e.shiftKey && e.key === "ArrowRight") { e.stopPropagation(); e.preventDefault(); secJump(1); return; }
      if (e.shiftKey && e.key === "ArrowLeft") { e.stopPropagation(); e.preventDefault(); secJump(-1); return; }
      // going BACK never lands on a finished animation: rewind one build step,
      // and from a slide's start jump to the previous subsection's beginning
      if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.stopPropagation(); e.preventDefault();
        var av = R.availableFragments();
        if (av && av.prev) R.prevFragment();
        else subPrev();
      }
    }, true);
    // ---- section-divider moments -----------------------------------------
    // a brief static title card when a NEW section is entered; pure overlay,
    // never touches slide or fragment state
    var divider = document.createElement("div");
    divider.className = "deck-divider";
    divider.innerHTML = '<div class="dd-kicker"></div><div class="dd-name"></div>';
    document.body.appendChild(divider);
    var divTimer = null, lastH = R.getIndices().h;
    function flashDivider(h) {
      var name = secName(h);
      if (!name) return;
      divider.querySelector(".dd-kicker").textContent = (h + 1) + " / " + stacks().length;
      divider.querySelector(".dd-name").textContent = name;
      divider.classList.add("show");
      clearTimeout(divTimer);
      divTimer = setTimeout(function () { divider.classList.remove("show"); }, 1100);
    }
    R.on("slidechanged", function () {
      var h = R.getIndices().h;
      if (h !== lastH && !(R.isOverview && R.isOverview())) flashDivider(h);
      lastH = h;
    });

    // ---- segmented progress bar ------------------------------------------
    // one segment per section, width proportional to its subsection count;
    // click a segment to jump to that section's start
    var prog = document.createElement("div");
    prog.className = "deck-progress";
    var fills = stacks().map(function (s, h) {
      var seg = document.createElement("div");
      seg.className = "dp-seg";
      seg.style.flexGrow = String(stackLen(h));
      seg.title = secName(h);
      var fill = document.createElement("div");
      fill.className = "dp-fill";
      seg.appendChild(fill);
      seg.addEventListener("click", function () { R.slide(h, 0, -1); });
      prog.appendChild(seg);
      return fill;
    });
    document.body.appendChild(prog);
    function updateProgress() {
      var i = R.getIndices();
      fills.forEach(function (fill, h) {
        var w = h < i.h ? 100 : h > i.h ? 0 : Math.round((i.v + 1) / stackLen(h) * 100);
        fill.style.width = w + "%";
      });
    }

    function refresh() { update(); updateProgress(); }
    R.on("slidechanged", refresh);
    R.on("fragmentshown", refresh);
    R.on("fragmenthidden", refresh);
    R.on("overviewshown", function () { el.style.display = "none"; });
    R.on("overviewhidden", function () { el.style.display = ""; });
    if (R.isReady()) refresh(); else R.on("ready", refresh);
  }

  return { init: init };
})();
