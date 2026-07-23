(() => {
  const pages = [
    ["/", "About", "⌂"],
    ["/news/", "News", "◇"],
    ["/cv/", "CV", "▤"],
    ["/research/", "Research", "⌬"],
    ["/activities/", "Activities", "◌"],
    ["/publications/", "Publications", "▥"],
    ["/teaching/", "Teaching", "♙"],
  ];

  const current = document.body.dataset.page;
  const nav = pages
    .map(([href, label, icon]) => {
      const active = current === label.toLowerCase() ? ' class="active"' : "";
      return `<a${active} href="${href}"><span class="nav-icon" aria-hidden="true">${icon}</span>${label}</a>`;
    })
    .join("");

  document.querySelector("#site-header").innerHTML = `
    <div class="nav-inner">
      <a class="brand" href="/">Ruidong Li</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <nav id="primary-navigation" class="primary-nav" aria-label="Primary navigation">${nav}</nav>
    </div>`;

  document.querySelector("#profile-panel").innerHTML = `
    <img class="profile-photo" src="/assets/img/profile/ruidong-li.webp" alt="Portrait of Ruidong Li">
    <div class="profile-copy">
      <p class="profile-role">Ph.D. Candidate<br>Geotechnical Engineering</p>
      <p>The Hong Kong<br>Polytechnic University</p>
    </div>
    <div class="contact-block">
      <h2>Contact</h2>
      <a href="mailto:rui-dong.li@connect.polyu.hk">rui-dong.li@connect.polyu.hk</a>
    </div>
    <div class="social-links" aria-label="Academic profiles">
      <a href="https://www.linkedin.com/in/ruidong-li-25b0b628b/" target="_blank" rel="noreferrer" aria-label="Ruidong Li on LinkedIn" title="LinkedIn" class="linkedin"><i class="brand-icon icon-linkedin" aria-hidden="true"></i></a>
      <a href="https://www.researchgate.net/profile/Ruidong-Li-5?ev=hdr_xprf" target="_blank" rel="noreferrer" aria-label="Ruidong Li on ResearchGate" title="ResearchGate" class="researchgate"><i class="brand-icon icon-researchgate" aria-hidden="true"></i></a>
      <a href="https://scholar.google.com/citations?user=FwgutEcAAAAJ&hl=en" target="_blank" rel="noreferrer" aria-label="Ruidong Li on Google Scholar" title="Google Scholar" class="google-scholar"><i class="icon-scholar" aria-hidden="true">G</i></a>
      <a href="https://github.com/li-ruidong" target="_blank" rel="noreferrer" aria-label="Ruidong Li on GitHub" title="GitHub" class="github"><i class="brand-icon icon-github" aria-hidden="true"></i></a>
    </div>`;

  document.querySelector("#site-footer").textContent =
    `© ${new Date().getFullYear()} Ruidong Li.`;

  const toggle = document.querySelector(".menu-toggle");
  const primaryNav = document.querySelector(".primary-nav");
  toggle.addEventListener("click", () => {
    const open = primaryNav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
})();
