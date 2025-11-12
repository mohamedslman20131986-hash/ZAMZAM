/* script.js — ذكي + يدوي (fallback)
   يحاول جلب ملفات .py من المستودع تلقائياً. إذا فشل يستخدم قائمة يدوية.
   الصق هذا الملف كـ script.js في جذر مستودع ZAMZAM.
*/

// ======= إعدادات (عدّل فقط إذا تغير اسم المستخدم/المستودع/الفرع أو مكان الملفات) =======
const OWNER = "mohamedslman20131986-hash";
const REPO  = "ZAMZAM";
const BRANCH = "main";
// إذا ملفاتك داخل مجلد فرعي داخل الريبو (مثال: "python-files") ضع إسمه هنا.
// إن كانت الملفات في الجذر اتركه ""
const FOLDER_PATH = ""; // مثال: "python-files" أو "" للجذر
// =======================================================================================

// قائمة يدوية احتياطية (لو فشل API أو تبي تتحكم بالأسماء بنفسك).
// غيّر/أضف أسماء الملفات كما هي موجودة في الريبو.
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

// عنصر الحاوية في الصفحة
const containerId = "files-container";

function showMessage(msg, isError = false) {
  const c = document.getElementById(containerId);
  if (!c) return;
  c.innerHTML = `<p style="color:${isError? '#ff9b9b':'#9ff3ff'}; text-align:center; margin-top:30px">${msg}</p>`;
}

// يبني رابط raw صالح للتحميل بناءً على مسار الملف في الريبو
function rawUrlFor(path) {
  // path قد يحتوي مجلد/اسم file.py أو مجرد اسم الملف
  return `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/${encodeURIComponent(path)}`;
}

// يعرض القائمة بشكل جميل
function renderList(items) {
  const c = document.getElementById(containerId);
  if (!c) return;
  if (!items || items.length === 0) {
    c.innerHTML = `<p class="loading">⚠️ لا توجد ملفات .py حالياً</p>`;
    return;
  }
  const colors = ['accent-blue','accent-pink','accent-green','accent-gold','accent-purple'];
  let html = '<div class="file-list">';
  items.forEach((it, i) => {
    // إذا العنصر هو سلسلة اسم فقط، حوّله لكائن مع download_url
    let name, download;
    if (typeof it === 'string') {
      name = it;
      download = rawUrlFor(it);
    } else {
      name = it.name || it.path || it;
      download = it.download_url || rawUrlFor(it.name || it.path || it);
    }
    const cClass = colors[i % colors.length];
    const sizeText = it.size ? `${it.size} بايت` : '';
    html += `<div class="file ${cClass}"><h3>${name}</h3><div class="meta">${sizeText}</div><a class="download" href="${download}" download>⬇️ تحميل</a></div>`;
  });
  html += '</div>';
  c.innerHTML = html;
}

// يحاول جلب الملفات من endpoint: /contents/{path}
// يعيد مصفوفة عناصر تحتوي {name, download_url, size}
async function fetchContentsPath(pathSegment) {
  const path = pathSegment ? encodeURIComponent(pathSegment) : "";
  const url = `https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}`;
  const res = await fetch(url, { headers: { 'Accept': 'application/vnd.github.v3+json' }});
  if (!res.ok) throw new Error(`contents fetch failed: ${res.status}`);
  const data = await res.json();
  // data قد يكون ملف واحد أو مصفوفة; نتأكد نرجع مصفوفة
  if (!Array.isArray(data)) return [];
  return data.filter(f => f.name && f.name.toLowerCase().endsWith('.py'))
             .map(f => ({ name: f.name, download_url: f.download_url, size: f.size }));
}

// خيار أقوى: استخدام git/trees?recursive=1 لقراءة كل الملفات بالريبو (يشمل المجلدات الفرعية)
async function fetchFromTreeRecursive() {
  const url = `https://api.github.com/repos/${OWNER}/${REPO}/git/trees/${BRANCH}?recursive=1`;
  const res = await fetch(url, { headers: { 'Accept': 'application/vnd.github.v3+json' }});
  if (!res.ok) throw new Error(`git/trees fetch failed: ${res.status}`);
  const data = await res.json();
  if (!data.tree) return [];
  // نبحث عن كل الملفات التي تنتهي بـ .py ونبني download_url حسب مسارها (path)
  const py = data.tree.filter(t => t.path && t.path.toLowerCase().endsWith('.py'))
                      .map(t => ({ name: t.path, download_url: rawUrlFor(t.path), size: t.size || 0 }));
  return py;
}

// الدالة الرئيسية التي تحاول عدة طرق ثم تستخدم fallback اليدوي
async function loadFiles() {
  const c = document.getElementById(containerId);
  if (!c) {
    console.error("لا يوجد عنصر بالصفحة بالـ id:", containerId);
    return;
  }

  showMessage('⏳ جاري البحث عن ملفات .py في المستودع...');

  // 1) إذا المستخدم حدد folder path (مثلاً "main" أو "python-files") نحاول جلب من هناك أولاً
  try {
    if (FOLDER_PATH && FOLDER_PATH.trim() !== "") {
      // جرب contents على المجلد المحدد
      const items = await fetchContentsPath(FOLDER_PATH);
      if (items && items.length > 0) {
        renderList(items);
        return;
      }
      // إن لم توجد، نجرب git/trees كاحتياط
      const fromTree = await fetchFromTreeRecursive();
      // فلتر على الملفات اللي بها نفس البادئة folderPath
      const filtered = fromTree.filter(f => f.name.startsWith(FOLDER_PATH + "/"));
      if (filtered.length > 0) {
        renderList(filtered);
        return;
      }
    } else {
      // 2) إذا FOLDER_PATH فارغ، جرب جلب محتويات الجذر
      const rootItems = await fetchContentsPath("");
      if (rootItems && rootItems.length > 0) {
        renderList(rootItems);
        return;
      }
      // 3) كخطة بديلة جرب git/trees recursive لالتقاط كل الملفات
      const all = await fetchFromTreeRecursive();
      if (all && all.length > 0) {
        renderList(all);
        return;
      }
    }
  } catch (err) {
    console.warn("GitHub API attempt failed:", err);
    // نستمر إلى fallback اليدوي أدناه
  }

  // إذا وصلنا هنا => كل محاولات API فشلت أو لم تُرجع ملفات مفيدة
  // نستخدم القائمة اليدوية manualFiles (تأكد أن الأسماء صحيحة ومطابقة تمامًا)
  if (manualFiles && manualFiles.length > 0) {
    showMessage('⚠️ لم يُسمح بالوصول للـ GitHub API — عرض القائمة اليدوية بدلاً عنه.');
    // نبني كائنات لRender (نضع download_url صالح)
    const items = manualFiles.map(n => ({ name: n, download_url: rawUrlFor(n), size: 0 }));
    renderList(items);
    return;
  }

  // النهاية: لا شيء وجد
  showMessage('⚠️ لم يتم العثور على ملفات .py — جرّب إضافة القائمة اليدوية manualFiles داخل script.js', true);
}

// شغّل التحميل عند التحميل الكامل للصفحة
document.addEventListener('DOMContentLoaded', loadFiles);
