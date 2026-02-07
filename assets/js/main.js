(function () {
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const DATA = window.KHALED_DATA;

  // --- Profile Populating ---
  $('#name').innerHTML = `Khaled <span>Djellali</span>`;
  // Subtitle will be handled by Typing Effect
  $('#aboutText').textContent = DATA.profile.about;
  $('#avatar').src = DATA.profile.photo;
  $('#loc').textContent = '📍 ' + DATA.profile.location;

  // Update Contact Links
  const mailLink = $('#mail a');
  if (mailLink) {
    mailLink.href = 'mailto:' + DATA.profile.email;
    mailLink.textContent = DATA.profile.email;
  }

  $('#phone').textContent = '📞 ' + DATA.profile.phone;
  $('#cvLink').href = DATA.profile.cv;
  $('#footName').textContent = DATA.profile.name;
  $('#year').textContent = new Date().getFullYear();

  // --- Typing Effect ---
  const typingElement = $('#subtitle');
  const typingTexts = [
    DATA.profile.subtitle,
    "Passionné par le développement Java & Web",
    "Futur Architecte de Systèmes d’Information"
  ];
  let textIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typeSpeed = 100;

  function type() {
    const currentText = typingTexts[textIndex];

    if (isDeleting) {
      typingElement.textContent = currentText.substring(0, charIndex - 1);
      charIndex--;
      typeSpeed = 50;
    } else {
      typingElement.textContent = currentText.substring(0, charIndex + 1);
      charIndex++;
      typeSpeed = 100;
    }

    if (!isDeleting && charIndex === currentText.length) {
      isDeleting = true;
      typeSpeed = 2000; // Pause at end
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      textIndex = (textIndex + 1) % typingTexts.length;
      typeSpeed = 500;
    }

    setTimeout(type, typeSpeed);
  }
  // Start typing effect
  type();


  // --- Skills Generation ---
  const skillsGrid = $('#skillsGrid');
  skillsGrid.className = 'skills-grid';
  skillsGrid.innerHTML = '';

  DATA.skills.forEach(s => {
    const card = document.createElement('div');
    card.className = 'skill-card';
    card.dataset.level = s.level;

    card.innerHTML = `
      <span class="skill-name">${s.name}</span>
      <span class="skill-level">${s.level}%</span>
      <div class="skill-bar">
        <div class="skill-fill" style="width: 0%"></div>
      </div>
    `;
    skillsGrid.appendChild(card);
  });

  // --- Experience / Timeline Generation ---
  const timeline = $('#timeline');
  timeline.innerHTML = '';

  DATA.experiences.forEach(e => {
    const item = document.createElement('li');
    item.className = 'timeline-item';
    const pointsList = e.points.map(p => `<li>${p}</li>`).join('');

    item.innerHTML = `
      <div class="timeline-content">
        <span class="timeline-date">${e.date}</span>
        <h3 class="timeline-title">${e.title}</h3>
        <div class="timeline-place">${e.univ}</div>
        <ul class="timeline-list">
          ${pointsList}
        </ul>
      </div>
    `;
    timeline.appendChild(item);
  });

  // --- Projects Generation & Filtering ---
  const projectsList = $('#projectsList');

  function renderProjects(filter = 'all') {
    projectsList.innerHTML = '';

    const filteredProjects = (filter === 'all')
      ? DATA.projects
      : DATA.projects.filter(p => p.category === filter);

    filteredProjects.forEach((p, i) => {
      // Find original index in DATA.projects for modal reference
      const originalIndex = DATA.projects.indexOf(p);

      const card = document.createElement('div');
      card.className = 'project-card';

      const imageHtml = (p.images && p.images.length > 0)
        ? `<img src="${p.images[0]}" alt="${p.name}" class="project-thumb">`
        : `<div class="project-thumb placeholder" style="background:#ccc;display:flex;align-items:center;justify-content:center;"><span>Aperçu</span></div>`;

      const codeBtn = (p.code && p.code !== '#')
        ? `<a class="project-btn code" href="${p.code}" target="_blank" rel="noopener noreferrer">Code</a>`
        : '';

      card.innerHTML = `
        <div class="project-thumb-wrapper">
          ${imageHtml}
        </div>
        <div class="project-info">
          <h3 class="project-title">${p.name}</h3>
          <p class="project-desc">${p.desc}</p>
          <div class="project-actions">
            <button class="project-btn details" data-index="${originalIndex}">Détails</button>
            ${codeBtn}
          </div>
        </div>
      `;
      projectsList.appendChild(card);
    });

    // Re-attach listeners
    projectsList.querySelectorAll('.details').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const idx = parseInt(e.currentTarget.dataset.index, 10);
        showProjectDetail(idx);
      });
    });
  }

  // Initial render
  renderProjects('all');

  // Filter Buttons Logic
  $$('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active class
      $$('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Filter logic
      const filterValue = btn.getAttribute('data-filter');

      // Minimal animation: fade out, render, fade in
      projectsList.style.opacity = '0';
      setTimeout(() => {
        renderProjects(filterValue);
        projectsList.style.opacity = '1';
      }, 200);
    });
  });


  // --- Modal Logic ---
  function showProjectDetail(i) {
    const p = DATA.projects[i];
    if (!p) return;

    const existing = $('.modal-overlay');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';

    const imagesHtml = (p.images || []).map(src => `<img src="${src}" alt="${p.name}">`).join('');
    const codeBtn = (p.code && p.code !== '#')
      ? `<a class="btn primary" href="${p.code}" target="_blank">Voir le Code Source</a>`
      : '';

    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">${p.name}</h2>
          <button class="modal-close">✕</button>
        </div>
        <div class="modal-body">
          <p class="modal-desc">${p.longDesc ? p.longDesc : p.desc}</p>
          <div class="modal-gallery">
            ${imagesHtml}
          </div>
          <div style="margin-top:30px; text-align:center;">
            ${codeBtn}
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';

    const close = () => {
      modal.style.opacity = '0';
      setTimeout(() => modal.remove(), 300);
      document.body.style.overflow = '';
    };

    modal.querySelector('.modal-close').addEventListener('click', close);
    modal.addEventListener('click', (e) => { if (e.target === modal) close(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
  }

  // --- Stats Counter Animation ---
  const statsSection = $('.stats-section');
  let statsAnimated = false; // Ensure it runs only once

  // --- Animations & Intersections ---
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');

        // Skill bars animation
        if (entry.target.id === 'skills') {
          $$('.skill-card').forEach(card => {
            const bar = card.querySelector('.skill-fill');
            if (bar) bar.style.width = card.dataset.level + '%';
          });
        }
      }
    });
  }, { threshold: 0.15 });

  $$('.section').forEach(sec => observer.observe(sec));

  // Separate observer for Stats to handle counting
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !statsAnimated) {
        statsAnimated = true;
        $$('.stat-number').forEach(stat => {
          const target = +stat.getAttribute('data-target');
          const duration = 2000; // ms
          const increment = target / (duration / 16); // 60fps

          let current = 0;
          const updateCount = () => {
            current += increment;
            if (current < target) {
              stat.textContent = Math.ceil(current);
              requestAnimationFrame(updateCount);
            } else {
              stat.textContent = target;
            }
          };
          updateCount();
        });
      }
    });
  }, { threshold: 0.5 });

  if (statsSection) statsObserver.observe(statsSection);

  // --- Scroll Progress ---
  const progress = $('.progress');
  window.addEventListener('scroll', () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const p = h > 0 ? (window.scrollY / h) : 0;
    progress.style.transform = `scaleX(${p})`;
  });

  // --- Mobile Menu ---
  const menuBtn = $('.menuBtn');
  const links = $('.links');

  menuBtn.addEventListener('click', () => {
    links.style.display = (links.style.display === 'flex') ? 'none' : 'flex';
    links.classList.toggle('open');
    menuBtn.textContent = links.classList.contains('open') ? '✕' : '☰';
  });

  $$('.links a').forEach(a => {
    a.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        links.style.display = 'none';
        links.classList.remove('open');
        menuBtn.textContent = '☰';
      }
    });
  });

  // --- Theme Toggle ---
  const root = document.documentElement;
  const themeToggle = $('#themeToggle');
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    root.classList.toggle('light', savedTheme === 'light');
  }

  function updateThemeIcon() {
    themeToggle.textContent = root.classList.contains('light') ? '🌙' : '☀️';
  }
  updateThemeIcon();

  themeToggle.addEventListener('click', () => {
    root.classList.toggle('light');
    const isLight = root.classList.contains('light');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    updateThemeIcon();
  });

  // --- Smooth Scroll ---
  $$('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

})();
