// assets/js/particles.js — Canvas particules animé
(function(){
  const c = document.getElementById('particles');
  if(!c) return;
  const ctx = c.getContext('2d');
  const resize = ()=>{ c.width = window.innerWidth; c.height = Math.min(520, window.innerHeight*0.7); };
  resize();
  window.addEventListener('resize', resize);

  const particles = Array.from({length: 80}, ()=> ({
    x: Math.random()*c.width,
    y: Math.random()*c.height,
    r: Math.random()*2+1,
    dx: (Math.random()-.5)*0.8,
    dy: (Math.random()-.5)*0.8
  }));

  function draw(){
    const g = ctx.createLinearGradient(0,0,c.width,c.height);
    g.addColorStop(0,'#0ea5e9'); g.addColorStop(1,'#38bdf8');
    ctx.fillStyle = g; ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle = 'rgba(255,255,255,.9)';
    particles.forEach(p=>{
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
      p.x += p.dx; p.y += p.dy;
      if(p.x<0||p.x>c.width) p.dx*=-1;
      if(p.y<0||p.y>c.height) p.dy*=-1;
    });
    requestAnimationFrame(draw);
  }
  draw();
})();