/* "Annotated paper" look: numbered rail labels, section numerals and §-style eyebrows. Runs after the deck script. */
(() => {
  const SEC = {
    "Introduction": ["1", "Intro", "book"], "Usage scenario": ["2", "Scenario", "users"], "Architecture": ["3", "System", "sitemap"],
    "User study": ["4", "Study", "chart"], "Discussion": ["6", "Discuss", "message"], "Critical reflections": ["†", "Critique", "pencil"], "Extensions": ["+", "Extend", "plus"]
  };
  // outline icons (paths from Tabler Icons, MIT)
  const ICON = {
    book: '<path d="M3 19a9 9 0 0 1 9 0a9 9 0 0 1 9 0"/><path d="M3 6a9 9 0 0 1 9 0a9 9 0 0 1 9 0"/><path d="M3 6v13"/><path d="M12 6v13"/><path d="M21 6v13"/>',
    users: '<path d="M5 7a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"/><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/><path d="M21 21v-2a4 4 0 0 0 -3 -3.85"/>',
    sitemap: '<path d="M3 17a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v2a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"/><path d="M15 17a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v2a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"/><path d="M9 5a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v2a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"/><path d="M6 15v-1a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v1"/><path d="M12 9v3"/>',
    chart: '<path d="M3 13a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"/><path d="M15 9a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"/><path d="M9 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v14a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"/><path d="M4 20h14"/>',
    message: '<path d="M3 20l1.3 -3.9c-2.324 -3.437 -1.426 -7.872 2.1 -10.374c3.526 -2.501 8.59 -2.296 11.845 .48c3.255 2.777 3.695 7.266 1.029 10.501c-2.666 3.235 -7.615 4.215 -11.574 2.293l-4.7 1"/>',
    pencil: '<path d="M4 20h4l10.5 -10.5a2.828 2.828 0 1 0 -4 -4l-10.5 10.5v4"/><path d="M13.5 6.5l4 4"/>',
    plus: '<path d="M12 5v14"/><path d="M5 12h14"/>'
  };
  const sec = t => SEC[t] || ["", t];
  // rail entries: number + short name for the rail, full name for the narrow top bar
  $$("#tabs a").forEach(a => {
    const t = a.dataset.tab, [n, s, ic] = sec(t);
    a.innerHTML = `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${ICON[ic] || ""}</svg><span class="s">${esc(s)}</span><span class="t">${esc(t)}</span>`;
    a.title = t;
  });
  // outlined numeral behind each scene
  scenes.forEach(s => { const w = s.classList.contains("scene") && s.querySelector(":scope > .wrap"); const n = sec(s.dataset.tab)[0]; if (w && /\d/.test(n)) w.dataset.num = n; });
  // "2.1) Usage scenario" -> "§2.1 · Usage scenario" (keeps persona avatars in the eyebrow)
  $$(".eyebrow").forEach(e => {
    const tn = [...e.childNodes].find(n => n.nodeType === 3 && n.textContent.trim());
    if (tn) tn.textContent = tn.textContent.replace(/^\s*([\d.–]+)\)\s*/, "§$1 · ");
  });
  // each scene's key sentence gets a mustard marker
  $$(".key").forEach(k => { k.innerHTML = `<span class="mk">${k.innerHTML}</span>`; });
  // mark finished sections in the rail
  const base = setCur;
  setCur = function (i) {
    base(i);
    const links = $$("#tabs a"), on = links.findIndex(a => a.classList.contains("on"));
    links.forEach((a, j) => a.classList.toggle("done", on >= 0 && j < on));
  };
  setCur(curScene);
})();
