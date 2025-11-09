
document.addEventListener("DOMContentLoaded", function () {
    const sliderContainer = document.getElementById("slider");
    let currentIndex = 0;
    let headlines = [];

    async function fetchHeadlines() {
        try {
            const response = await fetch("/static/json/mansetler.json");
            if (!response.ok) throw new Error("Veri çekilemedi.");
            headlines = await response.json();
            updateSlider();
            setInterval(nextSlide, 4000); // 4 saniyede bir kaydır
        } catch (error) {
            console.error("Manşet verisi alınamadı:", error);
        }
    }

    function updateSlider() {
        if (headlines.length === 0) return;
        const item = headlines[currentIndex];
        sliderContainer.innerHTML = `
            <div class="slider-item">
                <img src="${item.resim}" alt="${item.baslik}" class="slider-image">
                <div class="slider-caption">
                    <h2>${item.baslik}</h2>
                    <p>${item.tarih} - ${item.kategori}</p>
                    <a href="${item.link}" class="slider-link">Haberi Gör</a>
                </div>
            </div>
        `;
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % headlines.length;
        updateSlider();
    }

    fetchHeadlines();
});
