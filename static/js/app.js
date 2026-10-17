document.querySelectorAll(".close").forEach(b=>b.addEventListener("click",()=>b.closest(".flash").remove()));
document.querySelectorAll("form[data-confirm]").forEach(f=>f.addEventListener("submit",e=>{if(!confirm(f.dataset.confirm))e.preventDefault()}));
setTimeout(()=>document.querySelectorAll(".flash").forEach(f=>{f.style.transition="opacity .3s";f.style.opacity="0";setTimeout(()=>f.remove(),300)}),5000);
