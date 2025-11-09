# 📁 MODÜL: train_scheduler.py
# 🧾 AÇIKLAMA: Alfonso modelini her gün saat 02:00'de otomatik eğitir

from apscheduler.schedulers.background import BackgroundScheduler
from ai_training.train_alfonso import alfonso_egitim_baslat


def planla():
    scheduler = BackgroundScheduler()
    scheduler.add_job(alfonso_egitim_baslat, 'cron', hour=2, minute=0)
    scheduler.start()
    print("🕑 Alfonso eğitim zamanlayıcısı aktif (02:00)")


# main.py içinde aşağıdaki gibi kullanılabilir:
# from train_scheduler import planla
# planla()
