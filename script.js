(function(){
  const manualFiles = [
  "GOOD~joop.py",
  "ahmed (3).py",
  "Plag fasé.py",
  "انستا11.py",
  "اداة يضيم بعلي.py",
  "اداه فيس زمزم1.py",
  "الروسي زمزم.py",
  "بيجي زمزم مدفوعه (1).py",
  "بيجي مدفوعه ربط فيس.py",
  "صوفي انستا (1).py",
  "صيد حسابات كلاش اوف كلانس زمزم.py",
  "فيس تيربو (1).py",
  "فيس يوب ميل.py",
  "نار😈.py",
  "يوزرات تلي كلاش مميز.py",
  "CAR💀Parking✨.py"
  ];

  const container = document.getElementById('files-container');

  function renderList(files){
    if(!files || files.length===0){
      container.innerHTML = '<p class="loading">⚠️ لا توجد ملفات .py حالياً</p>';
      return;
    }
    const colors = ['accent-blue','accent-pink','accent-green','accent-gold','accent-purple'];
    let html = '<div class="file-list">';
    files.forEach((name,i)=>{
      const c = colors[i % colors.length];
      const download = `https://raw.githubusercontent.com/mohamedslman20131986-hash/ZAMZAM/main/${encodeURIComponent(name)}`;
      html += `<div class="file ${c}"><h3>${name}</h3><div class="meta">الاسم كما في الريبو</div><a class="download" href="${download}" download>⬇️ تحميل</a></div>`;
    });
    html += '</div>';
    container.innerHTML = html;
  }

  // Render manual list directly
  document.addEventListener('DOMContentLoaded', ()=> renderList(manualFiles));
})();
