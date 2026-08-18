(() => {
  'use strict';

  const root = document.documentElement;
  const body = document.body;
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));

  // Keep copyright dates current without requiring a rebuild.
  $$('[data-current-year]').forEach((element) => {
    element.textContent = String(new Date().getFullYear());
  });

  // Header background after the first scroll pixels.
  const header = $('[data-site-header]');
  if (header) {
    const updateHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 16);
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });
  }

  // Theme switcher. The initial value is applied inline in <head> to avoid a flash.
  const themeToggle = $('[data-theme-toggle]');
  const themeMeta = $('meta[name="theme-color"]');

  const updateThemeControl = () => {
    const isLight = root.dataset.theme === 'light';
    if (themeToggle) {
      themeToggle.setAttribute('aria-label', isLight ? 'Activer le thème sombre' : 'Activer le thème clair');
      themeToggle.setAttribute('title', isLight ? 'Activer le thème sombre' : 'Activer le thème clair');
    }
    if (themeMeta) {
      themeMeta.setAttribute('content', isLight ? '#f4f7fb' : '#07111f');
    }
  };

  updateThemeControl();

  themeToggle?.addEventListener('click', () => {
    const nextTheme = root.dataset.theme === 'light' ? 'dark' : 'light';
    root.dataset.theme = nextTheme;
    try {
      localStorage.setItem('portfolio-theme', nextTheme);
    } catch (error) {
      // localStorage may be disabled; the current page can still switch theme.
    }
    updateThemeControl();
  });

  // Responsive menu with focus-safe keyboard behavior.
  const menuToggle = $('[data-menu-toggle]');
  const mobileNav = $('[data-mobile-nav]');
  const mobileQuery = window.matchMedia('(max-width: 860px)');
  let lastFocusedElement = null;

  const syncNavAvailability = () => {
    if (!mobileNav) return;
    const menuIsOpen = body.classList.contains('menu-open');
    mobileNav.inert = mobileQuery.matches && !menuIsOpen;
  };

  const closeMenu = ({ restoreFocus = false } = {}) => {
    body.classList.remove('menu-open');
    menuToggle?.setAttribute('aria-expanded', 'false');
    menuToggle?.setAttribute('aria-label', 'Ouvrir le menu');
    syncNavAvailability();
    if (restoreFocus && lastFocusedElement instanceof HTMLElement) {
      lastFocusedElement.focus();
    }
  };

  const openMenu = () => {
    lastFocusedElement = document.activeElement;
    body.classList.add('menu-open');
    menuToggle?.setAttribute('aria-expanded', 'true');
    menuToggle?.setAttribute('aria-label', 'Fermer le menu');
    syncNavAvailability();
    const firstLink = $('.nav-link', mobileNav || document);
    window.requestAnimationFrame(() => firstLink?.focus());
  };

  menuToggle?.addEventListener('click', () => {
    if (body.classList.contains('menu-open')) {
      closeMenu({ restoreFocus: true });
    } else {
      openMenu();
    }
  });

  $$('.primary-nav a').forEach((link) => {
    link.addEventListener('click', () => closeMenu());
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && body.classList.contains('menu-open')) {
      closeMenu({ restoreFocus: true });
    }
  });

  const handleViewportChange = () => {
    if (!mobileQuery.matches) closeMenu();
    syncNavAvailability();
  };

  mobileQuery.addEventListener?.('change', handleViewportChange);
  syncNavAvailability();

  // Reveal content progressively. The site stays fully visible when JavaScript is disabled.
  const revealElements = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 },
    );

    revealElements.forEach((element) => revealObserver.observe(element));
  } else {
    revealElements.forEach((element) => element.classList.add('is-visible'));
  }

  // Project category filters.
  const filterButtons = $$('[data-project-filter]');
  const projectCards = $$('[data-project-card]');
  const filterStatus = $('[data-filter-status]');

  if (filterButtons.length && projectCards.length) {
    filterButtons.forEach((button) => {
      button.addEventListener('click', () => {
        const filter = button.dataset.projectFilter || 'all';
        let visibleCount = 0;

        filterButtons.forEach((candidate) => {
          const isActive = candidate === button;
          candidate.classList.toggle('is-active', isActive);
          candidate.setAttribute('aria-pressed', String(isActive));
        });

        projectCards.forEach((card) => {
          const shouldShow = filter === 'all' || card.dataset.category === filter;
          card.classList.toggle('is-filtered', !shouldShow);
          if (shouldShow) visibleCount += 1;
        });

        if (filterStatus) {
          filterStatus.textContent = `${visibleCount} projet${visibleCount > 1 ? 's' : ''} affiché${visibleCount > 1 ? 's' : ''}`;
        }
      });
    });
  }

  // Highlight the home navigation item corresponding to the visible section.
  if (body.classList.contains('home-page') && 'IntersectionObserver' in window) {
    const trackedSections = ['about', 'skills', 'journey', 'projects']
      .map((id) => document.getElementById(id))
      .filter(Boolean);
    const navLinks = $$('.nav-link');

    const sectionObserver = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible) return;

        navLinks.forEach((link) => {
          const linkHash = new URL(link.href, window.location.href).hash;
          link.classList.toggle('is-active', linkHash === `#${visible.target.id}`);
        });
      },
      { rootMargin: '-28% 0px -56% 0px', threshold: [0.02, 0.15, 0.3] },
    );

    trackedSections.forEach((section) => sectionObserver.observe(section));
  }

  // Native-dialog image lightbox for project galleries.
  const lightbox = $('[data-lightbox]');
  const lightboxImage = $('[data-lightbox-image]');
  const lightboxCaption = $('[data-lightbox-caption]');
  const lightboxClose = $('[data-lightbox-close]');
  const galleryItems = $$('[data-gallery-item]');

  const closeLightbox = () => {
    if (!lightbox) return;
    if (typeof lightbox.close === 'function' && lightbox.open) {
      lightbox.close();
    } else {
      lightbox.removeAttribute('open');
    }
  };

  if (lightbox && lightboxImage && galleryItems.length) {
    galleryItems.forEach((item) => {
      item.addEventListener('click', () => {
        const source = item.dataset.src || '';
        const alternative = item.dataset.alt || 'Capture du projet';
        lightboxImage.setAttribute('src', source);
        lightboxImage.setAttribute('alt', alternative);
        if (lightboxCaption) lightboxCaption.textContent = alternative;

        if (typeof lightbox.showModal === 'function') {
          lightbox.showModal();
        } else {
          lightbox.setAttribute('open', '');
        }
        lightboxClose?.focus();
      });
    });

    lightboxClose?.addEventListener('click', closeLightbox);

    lightbox.addEventListener('click', (event) => {
      const bounds = lightbox.getBoundingClientRect();
      const clickedBackdrop =
        event.clientX < bounds.left ||
        event.clientX > bounds.right ||
        event.clientY < bounds.top ||
        event.clientY > bounds.bottom;
      if (clickedBackdrop) closeLightbox();
    });

    lightbox.addEventListener('close', () => {
      lightboxImage.removeAttribute('src');
      lightboxImage.setAttribute('alt', '');
      if (lightboxCaption) lightboxCaption.textContent = '';
    });
  }
})();
