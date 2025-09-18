(function(){
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const DATA = window.KHALED_DATA;

  $('#name').textContent = DATA.profile.name;
  $('#subtitle').textContent = DATA.profile.subtitle;
  $('#aboutText').textContent = DATA.profile.about;
  $('#avatar').src = DATA.profile.photo;
  $('#loc').textContent = '📍 ' + DATA.profile.location;
  $('#mailCta').href = 'mailto:' + DATA.profile.email;
  $('#mail').innerHTML = '✉️ <a href="mailto:'+DATA.profile.email+'">'+DATA.profile.email+'</a>';
  $('#phone').textContent = '📞 ' + DATA.profile.phone;
  $('#cvLink').href = DATA.profile.cv;
  $('#footName').textContent = DATA.profile.name;
  $('#year').textContent = new Date().getFullYear();

  const skillsGrid = $('#skillsGrid');
  DATA.skills.forEach(s=>{
    const card = document.createElement('div');
    card.className = 'card skill';
    card.dataset.level = s.level;
    card.innerHTML = `
      <div class="row">
        <strong>${s.name}</strong>
        <span>${s.level}%</span>
      </div>
      <div class="bar"><i style="width:0"></i></div>`;
    skillsGrid.appendChild(card);
  });

  const timeline = $('#timeline');
  DATA.experiences.forEach(e=>{
    const li = document.createElement('li');
    li.className = 'card';
    li.innerHTML = '<h3 class="title">'+e.title+'</h3> <br/> <h3 class="univ">'+e.univ+'</h3> <br/> <span class="date">'+e.date+'<br/><br/></span>';
    const ul = document.createElement('ul');
    ul.className = 'bullets';
    e.points.forEach(p=>{
      const it = document.createElement('li'); it.textContent = p; ul.appendChild(it);
    });
    li.appendChild(ul);
    timeline.appendChild(li);
  });

const projectsList = document.getElementById('projectsList');
DATA.projects.forEach((p,i)=>{
  const card = document.createElement('div');
  card.className = 'project';

  card.innerHTML = `
    <h3>${p.name}</h3>
    ${p.images && p.images.length > 0 
      ? `<img src="${p.images[0]}" alt="${p.name}" class="project-thumb">`
      : `<div class="project-thumb placeholder">Aperçu</div>`
    }
    <div class="actions">
      ${p.code && p.code !== '#' 
        ? `<a class="btn" href="${p.code}" target="_blank" rel="noopener noreferrer">Code</a>` 
        : ''
      }
      <button class="btn demoBtn" data-index="${i}">Démo</button>
    </div>
  `;

  projectsList.appendChild(card);
});

projectsList.querySelectorAll('.demoBtn').forEach(btn=>{
  btn.addEventListener('click', (e)=>{
    const i = parseInt(e.currentTarget.dataset.index, 10);
    if(window.showProjectDetail) window.showProjectDetail(i);
  });
});

  const io = new IntersectionObserver(entries=>{
    entries.forEach(ent=>{
      if(ent.isIntersecting){
        ent.target.classList.add('visible');
        if(ent.target.id === 'skills' || ent.target.classList.contains('skills')){
          $$('.skill').forEach(el=>{
            el.querySelector('i').style.width = el.dataset.level + '%';
          });
        }
      }
    });
  },{threshold:.25});
  $$('.section').forEach(sec=>io.observe(sec));
  const progress = $('.progress');
  const onScroll = ()=>{
    const h = document.documentElement.scrollHeight - innerHeight;
    const p = h>0 ? (scrollY / h) : 0;
    progress.style.transform = 'scaleX('+p+')';
  };
  addEventListener('scroll', onScroll); onScroll();
  $('.toTop').addEventListener('click', ()=>scrollTo({top:0,behavior:'smooth'}));

  const menuBtn = $('.menuBtn'), links = $('.links');
  menuBtn.addEventListener('click', ()=>{
    const open = links.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open?'true':'false');
  });
  $$('.links a').forEach(a=>a.addEventListener('click', ()=>links.classList.remove('open')));

  const root = document.documentElement;
  const saved = localStorage.getItem('theme');
  if(saved) root.classList.toggle('light', saved==='light');
  const themeToggle = $('#themeToggle');
  themeToggle.addEventListener('click', ()=>{
    const light = !root.classList.contains('light');
    root.classList.toggle('light', light);
    localStorage.setItem('theme', light?'light':'dark');
    themeToggle.textContent = light ? '🌙' : '☀️';
  });
  themeToggle.textContent = root.classList.contains('light') ? '🌙' : '☀️';

  window.showProjectDetail = function(i){
    const p = DATA.projects[i];
    if(!p) return;
    const prev = document.getElementById('projectModal');
    if(prev) prev.remove();

    const modal = document.createElement('div');
    modal.id = 'projectModal';
    modal.className = 'modalOverlay';
    modal.innerHTML = `
      <div class="modalContent" role="dialog" aria-modal="true" aria-label="${p.name}">
        <button class="modalClose" aria-label="Fermer">✕</button>
        <h3>${p.name}</h3>
        <p class="modalDesc">${p.longDesc ? p.longDesc : p.desc}</p>
        <div class="modalImages">
          ${(p.images || []).map(src=>`<img src="${src}" alt="${p.name}">`).join('')}
        </div>
        <div class="modalActions">
          ${(p.code && p.code !== '#') ? `<a class="btn" target="_blank" rel="noopener noreferrer" href="${p.code}">Voir le code</a>` : ''}
          <button class="btn" id="modalCloseBtn">Fermer</button>
        </div>
      </div>`;
    document.body.appendChild(modal);
    modal.querySelector('.modalClose').addEventListener('click', ()=>modal.remove());
    modal.querySelector('#modalCloseBtn').addEventListener('click', ()=>modal.remove());
    modal.addEventListener('click', (e)=>{ if(e.target === modal) modal.remove(); });
    document.addEventListener('keydown', (ev)=>{ if(ev.key === 'Escape'){ modal.remove(); } });
  };
})();
