// إعدادات GitHub API
const username = "mohamedsIman20131986-hash";
const repo = "ZAMZAM";

const container = document.getElementById("files-container");

async function loadFiles() {
  try {
    const response = await fetch(`https://api.github.com/repos/${username}/${repo}/contents/`);
    if (!response.ok) throw new Error("خطأ في الاتصال بـ GitHub API");

    const files = await response.json();
    const pyFiles = files.filter(file => file.name.endsWith(".py"));

    if (pyFiles.length === 0) {
      container.innerHTML = `<p class="loading">⚠️ حالياً لم يتم العثور على ملفات .py</p>`;
      return;
    }

    let html = `<div class="file-list">`;
    pyFiles.forEach(file => {
      html += `
        <div class="file">
          <h3>${file.name}</h3>
          <a class="download" href="${file.download_url}" download>⬇️ تحميل</a>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  } catch (error) {
    container.innerHTML = `<p class="loading">⚠️ حدث خطأ أثناء تحميل الملفات.</p>`;
    console.error(error);
  }
}

loadFiles();
