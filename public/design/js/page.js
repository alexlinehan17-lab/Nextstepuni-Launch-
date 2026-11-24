// the dark greys actually found in the code
const B=['#09090b','#0a0a0a','#0f0f0e','#131313','#141413','#141414','#141416','#151515','#171717','#181818','#18181b','#181b18','#191919','#1b1b1b','#1b1b1e','#1c1c1c','#1d1c1b','#1d1d1b','#1f1f23','#20201d','#20201f','#202020','#20211e','#201F1D','#212121','#222220','#232720','#242720','#242321','#242424','#252422','#252525','#262626','#27272a','#282624','#282828','#292929','#292725','#2a2927','#2a2825','#2b2927','#2b2b2b','#2d2b28','#303030'];
document.getElementById('blacks').innerHTML=B.map(c=>`<i style="background:${c}" title="${c}"></i>`).join('');
// the dark-mode pair is always dark
document.querySelectorAll('.darkpair').forEach(e=>e.classList.add('darkmocks'));
// Future Finder demo starts with nothing selected
document.querySelectorAll('[data-opt=none] .ans').forEach(a=>a.setAttribute('aria-pressed','false'));
