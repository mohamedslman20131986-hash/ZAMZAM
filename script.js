// script.js (ذكي) - يحاول جلب ملفات .py تلقائياً من GitHub، مع fallback إلى files.json
(async function(){
  const username = "mohamedsIman20131986-hash"; // اسم المستخدم
  const repo = "ZAMZAM";                        // اسم المستودع
  const branch = "main";                        // الفرع
  const container = document.getElementById('files-container');

  function showMessage(msg, isErr=false){
    container.innerHTML = `<p class="loading" style="color:${isErr? '#ff9b9b':'#9ff3ff'}">${msg}</p>`;
  }

  // يبني رابط تحميل raw من اسم الملف
  function rawUrlFor(name){
    return `https://raw.githubusercontent.com/${username}/${repo}/${branch}/${encodeURIComponent(name)}`;
  }

  // يـحاول استخدام git/trees (recursive) — يعطي قائمة كل الملفات في الريبو (أفضل من contents)
  async function fetchFromTree(){
    const url = `https://api.github.com/repos/${username}/${repo}/git/trees/${branch}?recursive=1`;
    const res = await fetch(url, { headers: { 'Accept': 'application/vnd.github.v3+json' }});
    if(!res.ok) throw new Error('git/trees fetch failed: ' + res.status);
    const data = await res.json();
    // data.tree => array of { path, mode, type, sha, size, url }
    const py = data.tree.filter(f => f.path && f.path.toLowerCase().endsWith('.py'));
    return py.map(f => ({ name: f.path, download_url: rawUrlFor(f.path), size: f.size || 0 }));
  }

  // fallback: جلب ملف files.json (تضعه يدوياً بالمستودع root إذا احتجت)
  async function fetchFromFilesJson(){
    const url = `https://raw.githubusercontent.com/${username}/${repo}/${branch}/files.json`;
    const res = await fetch(url);
    if(!res.ok) throw new Error('files.json not found or fetch failed: ' + res.status);
    const data = await res.json(); // متوقع مصفوفة من {name, download_url, size?}
    return data;
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

  // التسلسل: نجرب git/trees أول، لو فشل نجرب files.json، لو فشل نعرض رسالة إرشادية
  try{
    showMessage('جاري تحميل قائمة الملفات من GitHub (git/trees)...');
    const files = await fetchFromTree();
    renderList(files);
  }catch(errTree){
    console.warn('git/trees failed:', errTree);
    try{
      showMessage('فشل git/trees. نجرب جلب files.json كاحتياط...');
      const files2 = await fetchFromFilesJson();
      renderList(files2);
    }catch(errJson){
      console.warn('files.json fetch failed:', errJson);
      // النهائي: نعرض تعليمات واضحة للمستخدم/لك لتصليح المشكلة
      container.innerHTML = `
        <p class="loading" style="color:#ff9b9b">⚠️ حدث خطأ أثناء الوصول لـ GitHub API أو files.json.</p>
        <p style="color:#ffdca6">حل سريع: افتح ملف <code>script.js</code> وأضف أسماء ملفات .py يدوياً في مصفوفة <code>manualFiles</code> أو أنشئ ملف <code>files.json</code> في الريبو.</p>
        <p style="color:#ffdca6;margin-top:10px">لإنشاء files.json تلقائياً: شغّل السكربت البسيط المرفق (Python) على جهازك ثم ارفع files.json إلى جذر المستودع.</p>
      `;
    }
  }
})();
