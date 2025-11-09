document.getElementById('csvForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/admin/upload-csv', {
        method: 'POST',
        body: formData
    });
    alert(response.ok ? 'CSV başarıyla yüklendi.' : 'CSV yüklenemedi.');
});

document.getElementById('trainAlfonso').addEventListener('click', async () => {
    const response = await fetch('/admin/train-alfonso', { method: 'POST' });
    alert(response.ok ? 'Eğitim başlatıldı.' : 'Eğitim başlatılamadı.');
});

document.getElementById('viewLogs').addEventListener('click', async () => {
    const response = await fetch('/admin/logs');
    const logText = await response.text();
    document.getElementById('logOutput').textContent = logText;
});

document.getElementById('haberForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/admin/haber-ekle', {
        method: 'POST',
        body: formData
    });
    alert(response.ok ? 'Haber eklendi!' : 'Haber eklenemedi.');
});

document.getElementById('bannerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/admin/banner-ekle', {
        method: 'POST',
        body: formData
    });
    alert(response.ok ? 'Banner kaydedildi!' : 'Banner eklenemedi.');
});
