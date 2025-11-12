document.addEventListener("DOMContentLoaded", function() {
  const fileList = document.getElementById("file-list");

  fetch("https://api.github.com/repos/mohamedsIman20131986-hash/mohamedsIman20131986-hash.github.io/contents/")
    .then(response => response.json())
    .then(files => {
      const pyFiles = files.filter(file => file.name.endsWith(".py"));
      if (pyFiles.length === 0) {
        fileList.innerHTML = "<p>⚠️ حالياً لم يتم العثور على ملفات .py</p>";
        return;
      }

      pyFiles.forEach(file => {
        const fileItem = document.createElement("div");
        fileItem.classList.add("file-item");

        const fileLink = document.createElement("a");
        fileLink.href = file.download_url;
        fileLink.textContent = file.name;
        fileLink.download = file.name;

        fileItem.appendChild(fileLink);
        fileList.appendChild(fileItem);
      });
    })
    .catch(err => {
      console.error("حدث خطأ أثناء تحميل الملفات:", err);
      fileList.innerHTML = "<p>⚠️ حدث خطأ أثناء تحميل الملفات.</p>";
    });
});
