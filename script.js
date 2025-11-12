/* script.js - تحميل مباشر لجميع الأجهزة (iPhone + Android + PC) */

// إعدادات المستودع
const OWNER = "mohamedslman20131986-hash";
const REPO = "ZAMZAM";
const BRANCH = "main";
const FOLDER_PATH = ""; // خليه فاضي إذا الملفات بالجذر

// أسماء الملفات اليدوية (احتياط في حال فشل API)
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

// العنصر اللي راح نعرض بيه الملفات
const containerId = "files-container";

// عرض رسالة
function showMessage(msg, isError = false) {
  const c = document.getElementById(containerId);
  if (c) c.innerHTML = `<p style="color:${isError ? "#ff8c8c" : "#9ff3ff"};text-align:center;">${msg}</p>`;
}

// بناء رابط raw مباشر
function rawUrlFor(path) {
  return `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/${encodeURIComponent(path)}`;
}

// تحميل الملف فعليًا
async function forceDownload(url, filename) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("فشل التحميل");
    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
  } catch (err) {
    alert("حدث خطأ أثناء التحميل ❌");
    console.error(err);
  }
}

// عرض قائمة الملفات
function renderFiles(files) {
  const c = document.getElementById(containerId);
  if (!c) return;
  const colors = ['accent-blue','accent-pink','accent-green','accent-gold','accent-purple'];
  let html = '<div class="file-list">';
  files.forEach((file, i) => {
    const name = file.name || file;
    const url = file.download_url || rawUrlFor(name);
    const color = colors[i % colors.length];
    html += `
      <div class="file ${color}">
        <h3>${name}</h3>
        <button onclick="forceDownload('${url}','${name}')">⬇️ تحميل مباشر</button>
      </div>`;
  });
  html += '</div>';
  c.innerHTML = html;
}

// جلب الملفات من GitHub API
async function fetchFiles() {
  try {
    showMessage("⏳ جارٍ جلب الملفات...");
    const path = FOLDER_PATH ? `/${FOLDER_PATH}` : "";
    const res = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents${path}`);
    if (!res.ok) throw new Error("API فشل");
    const data = await res.json();
    const pyFiles = data.filter(f => f.name.endsWith(".py"));
    renderFiles(pyFiles);
  } catch {
    const fallback = manualFiles.map(f => ({ name: f, download_url: rawUrlFor(f) }));
    renderFiles(fallback);
  }
}

document.addEventListener("DOMContentLoaded", fetchFiles);
