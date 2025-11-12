// script.js — يعرض ملفات .py الموجودة في مجلد الموقع مباشرة

const repoOwner = "mohamedslman20131986-hash";
const repoName = "ZAMZAM";

async function loadFiles() {
  const container = document.getElementById("files");

  try {
    const response = await fetch(`https://api.github.com/repos/${repoOwner}/${repoName}/contents/`);
    if (!response.ok) throw new Error("GitHub API error");

    const data = await response.json();
    const pyFiles = data.filter(file => file.name.endsWith(".py"));

    if (pyFiles.length === 0) {
      container.innerHTML = `<p style="color:yellow">⚠️ لا توجد ملفات Python حالياً</p>`;
      return;
    }

    container.innerHTML = pyFiles.map(file => `
      <a href="${file.download_url}" download class="file-item">
        🐍 ${file.name}
      </a>
    `).join("");

  } catch (err) {
    console.error(err);
    container.innerHTML = `
      <p style="color:#ff5555">
        ⚠️ حدث خطأ أثناء تحميل الملفات. 
        <br>إذا استمر الخطأ، أضف أسماء الملفات يدوياً في المصفوفة أدناه.
      </p>
    `;

    // النسخ الاحتياطي اليدوي (تقدر تضيف هنا الملفات يدوياً)
    const manualFiles = [
      // "file1.py",
      // "file2.py"
    ];
    if (manualFiles.length > 0) {
      container.innerHTML += manualFiles.map(name => `
        <a href="${name}" download class="file-item">🐍 ${name}</a>
      `).join("");
    }
  }
}

document.addEventListener("DOMContentLoaded", loadFiles);
