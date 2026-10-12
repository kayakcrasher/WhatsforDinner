/* Three independent recipe draws, with replacement; no paid odds or forced matches. */
let slotSound = localStorage.getItem('wfd_sound') === 'true';
let audioContext;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const tracks = [...document.querySelectorAll('.reel-track')];
const icons = {chicken:'🍗',beef:'🥩',pork:'🍖',seafood:'🍤',vegetarian:'🥦',lamb:'🍲'};

function tile(recipe, selectable = false) {
  const el = document.createElement(selectable ? 'button' : 'div');
  el.className = 'reel-tile' + (selectable ? ' reel-choice' : '');
  const icon = document.createElement('span');
  icon.className = 'reel-icon';
  icon.setAttribute('aria-hidden','true');
  icon.textContent = recipe ? icons[recipe.protein] || '🍽️' : '🍽️';
  const title = document.createElement('span');
  title.className = 'reel-title';
  title.textContent = recipe ? recipe.name : 'What sounds good?';
  el.append(icon,title);
  if(selectable) {
    el.type = 'button';
    el.setAttribute('aria-label','Choose '+recipe.name);
    el.addEventListener('click',()=>{
      currentRecipe = recipe;
      showRecipe(recipe);
      $('slotStatus').textContent = 'On the menu: '+recipe.name;
    });
  }
  return el;
}

function pick(pool) { return pool[Math.floor(Math.random()*pool.length)]; }

async function roll(track, pool, result, index) {
  const count = 16 + index*4;
  track.style.transform = 'translateY(0)';
  track.replaceChildren(...Array.from({length:count},()=>tile(pick(pool))),tile(result));
  track.setAttribute('aria-hidden','true');
  if(!reducedMotion.matches) {
    const animation = track.animate([
      {transform:'translateY(0)'},
      {transform:`translateY(-${count*150}px)`}
    ], {duration:1500+index*450,easing:'cubic-bezier(.12,.65,.12,1)',fill:'forwards'});
    await animation.finished;
    animation.cancel();
  }
  track.replaceChildren(tile(result,true));
  track.style.transform = 'translateY(0)';
  track.removeAttribute('aria-hidden');
  track.querySelector('button').disabled = true;
}

function celebrate() {
  $('slotMachine').classList.add('jackpot');
  $('marquee').textContent = 'THREE OF A KIND · DINNER JACKPOT!';
  if(!reducedMotion.matches) {
    const shower = document.createElement('div');
    shower.className = 'confetti';
    shower.setAttribute('aria-hidden','true');
    for(let i=0;i<60;i++) {
      const piece = document.createElement('i');
      piece.style.left = Math.random()*100+'%';
      piece.style.background = ['#ffc96b','#fc638d','#6ae0c4'][i%3];
      piece.style.animationDelay = Math.random()*.4+'s';
      piece.style.setProperty('--drift',(Math.random()-.5)*180+'px');
      shower.append(piece);
    }
    document.body.append(shower);
    setTimeout(()=>shower.remove(),3200);
  }
  if(slotSound && audioContext && audioContext.state === 'running') {
    [523.25,659.25,783.99,1046.5].forEach((frequency,index)=>{
      const tone = audioContext.createOscillator();
      const volume = audioContext.createGain();
      const start = audioContext.currentTime + index*.12;
      tone.frequency.value = frequency;
      volume.gain.setValueAtTime(.0001,start);
      volume.gain.exponentialRampToValueAtTime(.07,start+.015);
      volume.gain.exponentialRampToValueAtTime(.0001,start+.3);
      tone.connect(volume).connect(audioContext.destination);
      tone.start(start);tone.stop(start+.32);
    });
  }
}

async function spin() {
  if(isSpinning)return;
  isSpinning = true;
  const query = filterQuery(); // Freeze filters for this pull.
  const controls = [...document.querySelectorAll('.chip'),$('spinBtn'),$('lever')];
  const oldDisabled = controls.map(el=>el.disabled);
  controls.forEach(el=>el.disabled=true);
  tracks.forEach(track=>track.querySelectorAll('button').forEach(el=>el.disabled=true));
  $('lever').classList.add('pulled');
  $('slotMachine').classList.remove('jackpot');
  $('slotMachine').setAttribute('aria-busy','true');
  $('marquee').textContent = 'WHAT WILL BE ON YOUR MENU?';
  $('slotStatus').textContent = 'Finding three recipes for your filters…';
  $('spinBtn').textContent = 'Picking your next meal…';
  if(slotSound) {
    try {
      const Audio = window.AudioContext || window.webkitAudioContext;
      if(Audio) { audioContext ||= new Audio(); audioContext.resume().catch(()=>{}); }
    } catch(e) { /* Sound is optional. */ }
  }
  setTimeout(()=>$('lever').classList.remove('pulled'),450);
  const controller = new AbortController();
  const timeout = setTimeout(()=>controller.abort(),10000);
  try {
    const response = await fetch('/api/recipes'+query,{signal:controller.signal});
    if(!response.ok)throw new Error('Could not load recipes. Please try again.');
    const data = await response.json();
    clearTimeout(timeout);
    if(!data.recipes?.length)throw new Error('No recipes match. Try changing your filters.');
    const results = Array.from({length:3},()=>pick(data.recipes));
    $('slotStatus').textContent = 'Rolling… three delicious possibilities.';
    await Promise.all(tracks.map((track,index)=>roll(track,data.recipes,results[index],index)));
    currentRecipe = results[0];
    showRecipe(currentRecipe);
    if(results.every(recipe=>recipe.id===results[0].id)) {
      celebrate();
      $('slotStatus').textContent = 'Dinner jackpot! Three '+currentRecipe.name+' recipes lined up. Time to cook!';
    } else {
      $('marquee').textContent = 'THREE IDEAS · YOUR PICK';
      $('slotStatus').textContent = 'Dinner is served! Tap any reel to choose your recipe.';
    }
  } catch(error) {
    $('marquee').textContent = 'LET’S FIND SOMETHING DELICIOUS';
    $('slotStatus').textContent = error.name==='AbortError'
      ? 'That took too long. Check your connection and try again.'
      : error.message || 'Could not connect. Please try again.';
  } finally {
    clearTimeout(timeout);
    isSpinning = false;
    controls.forEach((el,index)=>el.disabled=oldDisabled[index]);
    tracks.forEach(track=>track.querySelectorAll('button').forEach(el=>el.disabled=false));
    $('lever').classList.remove('pulled');
    $('slotMachine').removeAttribute('aria-busy');
    $('spinBtn').textContent = 'Pull for dinner';
  }
}

tracks.forEach(track=>track.append(tile(null)));
$('spinBtn').addEventListener('click',spin);
$('lever').addEventListener('click',spin);
let dragStart = null;
$('lever').addEventListener('pointerdown',event=>{
  if(isSpinning)return;
  dragStart = event.clientY;
  $('lever').setPointerCapture(event.pointerId);
});
$('lever').addEventListener('pointermove',event=>{
  if(dragStart!==null && event.clientY-dragStart>30) {
    dragStart=null;
    spin();
  }
});
['pointerup','pointercancel'].forEach(name=>$('lever').addEventListener(name,()=>{dragStart=null;}));
