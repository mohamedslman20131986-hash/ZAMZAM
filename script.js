document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("files-container");
  const repo = "mohamedslman20131986-hash/ZAMZAM"; // اسم المستودع
  const branch = "main";

  container.innerHTML = "<p class='loading'>🔄 جارٍ تحميل الملفات...</p>";

  try {
    // جلب قائمة الملفات من GitHub API
    const response = await fetch(`https://api.github.com/repos/${repo}/contents/?ref=${branch}`);
    const files = await response.json();

    container.innerHTML = ""; // تفريغ المحتوى

    files
      .filter(file => file.name.endsWith(".py")) // عرض فقط ملفات بايثون
      .forEach(file => {
        const fileDiv = document.createElement("div");
        fileDiv.className = "file-item";

        const fileName = document.createElement("h3");
        fileName.textContent = file.name;

        const downloadBtn = document.createElement("button");
        downloadBtn.textContent = "⬇️ تحميل الملف";
        downloadBtn.onclick = async () => {
          try {
            const rawUrl = `https://raw.githubusercontent.com/${repo}/${branch}/${file.name}`;
            const res = await fetch(rawUrl);
            const blob = await res.blob();

            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = file.name;
            link.click();

            URL.revokeObjectURL(link.href);
          } catch (error) {
            alert("حدث خطأ أثناء التحميل");
          }
        };

        fileDiv.appendChild(fileName);
        fileDiv.appendChild(downloadBtn);
        container.appendChild(fileDiv);
      });

    if (container.innerHTML.trim() === "") {
      container.innerHTML = "<p>🚫 لا توجد ملفات بايثون حالياً.</p>";
    }
  } catch (error) {
    container.innerHTML = "<p>⚠️ حدث خطأ أثناء تحميل الملفات.</p>";
  }
});
