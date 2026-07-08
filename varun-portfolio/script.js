(() => {
  const root = document.documentElement;
  const themeToggle = document.getElementById("themeToggle");
  const STORAGE_KEY = "vk-theme";

  // ---------- Theme ----------
  function applyTheme(theme){
    root.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved){
    applyTheme(saved);
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches){
    applyTheme("dark");
  }

  themeToggle.addEventListener("click", () => {
    const current = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
    applyTheme(current === "dark" ? "light" : "dark");
  });

  // ---------- Mobile menu ----------
  const hamburger = document.getElementById("hamburger");
  const mobileMenu = document.getElementById("mobileMenu");
  hamburger.addEventListener("click", () => {
    mobileMenu.classList.toggle("open");
  });
  mobileMenu.querySelectorAll("a").forEach(a => {
    a.addEventListener("click", () => mobileMenu.classList.remove("open"));
  });

  // ---------- Nav shadow on scroll ----------
  const nav = document.getElementById("nav");
  window.addEventListener("scroll", () => {
    nav.style.boxShadow = window.scrollY > 8 ? "0 1px 0 rgba(0,0,0,0.04)" : "none";
  });

  // ---------- Count-up stats ----------
  const stats = document.querySelectorAll(".stat-num");
  let counted = false;
  function countUp(el){
    const target = parseInt(el.dataset.target, 10);
    const duration = 1200;
    const start = performance.now();
    function tick(now){
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target);
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const statsSection = document.getElementById("stats");
  if (statsSection){
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !counted){
          counted = true;
          stats.forEach(countUp);
        }
      });
    }, { threshold: 0.4 });
    io.observe(statsSection);
  }

  // ---------- Scroll reveal ----------
  const revealTargets = document.querySelectorAll(
    ".skill-card, .work-card, .testi-card, .about-text, .cta-card, .contact-card, .hero-visual, .hero-copy"
  );
  revealTargets.forEach(el => el.classList.add("reveal"));

  const revealIO = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting){
        entry.target.classList.add("in");
        revealIO.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  revealTargets.forEach(el => revealIO.observe(el));
})();
