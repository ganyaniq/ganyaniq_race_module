document.addEventListener("DOMContentLoaded", () => {
  // Bannerları getir
  fetch("/api/banners")
    .then(res => res.json())
    .then(data => {
      const track = document.getElementById("slider-track");
      data.banners.forEach(b => {
        const banner = document.createElement("a");
        banner.href = b.link;
        banner.target = "_blank";
        banner.className = "banner-item";
        banner.innerHTML = `<img src='/static/assets/${b.filename}' alt='banner'>`;
        track.appendChild(banner);
      });
    });

  // Haberleri getir
  fetch("/api/haberler")
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("haber-listesi");
      data.haberler.forEach(h => {
        const item = document.createElement("li");
        item.className = "haber-item";
        item.innerHTML = `<strong>${h.baslik}</strong><p>${h.icerik}</p>`;
        list.appendChild(item);
      });
    });
});
