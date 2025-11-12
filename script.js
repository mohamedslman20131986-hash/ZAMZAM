(async function(){
  const username = "mohamedsIman20131986-hash";
  const repo = "ZAMZAM";
  const container = document.getElementById('files-container');

  function showMessage(msg, isErr=false){
    container.innerHTML = `<p class="loading" style="color:${isErr? '#ff9b9b':'#9ff3ff'}">${msg}</p>`;
  }

  // fallback manual list: if GitHub API blocked, you can add filenames here (exact names)
  // Example: const manualFiles = ["GOOD~joop.py","ahmed (3).py"];
  const manualFiles = []; // <--- leave empty to try automatic; or add your filenames

  async function loadFromApi(){
    const url = `https://api.github.com/repos/${username}/${repo}/contents/`;
    const res = await fetch(url);
    if(!res.ok) throw new Error('API fetch failed: ' + res.status);
    const data = await res.json();
    const py = data.filter(f => f.name.endsWith('.py'));
    return py.map(f => ({name: f.name, download_url: f.download_url, size: f.size}));
  }

  function renderList(files){
    if(!files || files.length===0){ showMessage('⚠️ حالياً لم يتم العثور على ملفات .py'); return; }
    const colors = ['accent-blue','accent-pink','accent-green','accent-gold','accent-purple'];
    let html = '<div class="file-list">';
    files.forEach((f,i)=>{
      const c = colors[i % colors.length];
      html += `<div class="file ${c}"><h3>${f.name}</h3><div class="meta">حجم: ${f.size? f.size+' بايت':''}</div><a class="download" href="${f.download_url}" download>⬇️ تحميل</a></div>`;
    });
    html += '</div>';
    container.innerHTML = html;
  }

  try{
    showMessage('جاري التحميل من GitHub...');
    let files = [];
    if(manualFiles.length>0){
      // build download URLs for manual list
      files = manualFiles.map(n=>({name:n, download_url:`https://raw.githubusercontent.com/${username}/${repo}/main/${encodeURIComponent(n)}`}));
    } else {
      files = await loadFromApi();
    }
    renderList(files);
  }catch(err){
    console.error(err);
    if(manualFiles.length>0){
      showMessage('تم تحميل القائمة يدوياً من التكوين المحلي.');
      const files = manualFiles.map(n=>({name:n, download_url:`https://raw.githubusercontent.com/${username}/${repo}/main/${encodeURIComponent(n)}`}));
      renderList(files);
    } else {
      showMessage('⚠️ حدث خطأ أثناء الوصول لـ GitHub API. أضف أسماء الملفات يدوياً داخل script.js (المتغير manualFiles).', true);
      // show empty list hint
      container.innerHTML += '<p style="color:#ffdca6;margin-top:14px">نصيحة: افتح ملف <code>script.js</code> وأضف أسماء ملفات .py في مصفوفة <code>manualFiles</code> إذا بقيت المشكلة.</p>';
    }
  }
})();