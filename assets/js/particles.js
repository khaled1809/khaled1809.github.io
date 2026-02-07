// assets/js/particles.js — Modern subtle particles
(function () {
  const canvas = document.getElementById('particles');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];

  // Configuration
  const particleCount = 60;
  const connectionDistance = 150;
  const mouseDistance = 200;

  let mouse = { x: null, y: null };

  window.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });

  window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
  });

  function resize() {
    width = canvas.width = canvas.parentElement.offsetWidth;
    height = canvas.height = canvas.parentElement.offsetHeight;
  }

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.5;
      this.vy = (Math.random() - 0.5) * 0.5;
      this.size = Math.random() * 2 + 1;
      this.color = 'rgba(56, 189, 248, '; // Using primary color variable base
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      // Bounce
      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;

      // Mouse interaction
      if (mouse.x != null) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < mouseDistance) {
          const forceDirectionX = dx / distance;
          const forceDirectionY = dy / distance;
          const force = (mouseDistance - distance) / mouseDistance;
          const directionX = forceDirectionX * force * 0.05;
          const directionY = forceDirectionY * force * 0.05;
          this.vx += directionX;
          this.vy += directionY;
        }
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = this.color + '0.5)';
      ctx.fill();
    }
  }

  function init() {
    resize();
    particles = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach(p => {
      p.update();
      p.draw();
    });

    connect();
    requestAnimationFrame(animate);
  }

  function connect() {
    for (let a = 0; a < particles.length; a++) {
      for (let b = a; b < particles.length; b++) {
        const dx = particles[a].x - particles[b].x;
        const dy = particles[a].y - particles[b].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < connectionDistance) {
          const opacity = 1 - (distance / connectionDistance);
          ctx.strokeStyle = 'rgba(56, 189, 248, ' + (opacity * 0.2) + ')';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(particles[a].x, particles[a].y);
          ctx.lineTo(particles[b].x, particles[b].y);
          ctx.stroke();
        }
      }
    }
  }

  window.addEventListener('resize', () => {
    resize();
    init();
  });

  init();
  animate();

})();