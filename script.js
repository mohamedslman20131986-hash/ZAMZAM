// توليد روابط التحميل تلقائياً لأي ملف .py
document.addEventListener('DOMContentLoaded', async () => {
  const listContainer = document.getElementById('file-list');
  const msg = document.getElementById('msg');

  try {
    const res = await fetch('.');
    const text = await res.text();
    const files = [...text.matchAll(/href="([^"]+\.py)"/g)].map(m => m[1]);

    if (!files.length) {
      listContainer.innerHTML = '<p>⚠️ لم يتم العثور على ملفات .py حالياً</p>';
      return;
    }

    files.forEach(file => {
      const div = document.createElement('div');
      div.className = 'file-item';
      div.innerHTML = `<span>${file}</span><a href="${file}" download>تحميل</a>`;
      listContainer.appendChild(div);
    });

  } catch (err) {
    console.error(err);
    msg.textContent = 'حدث خطأ أثناء تحميل القائمة';
  }
});
