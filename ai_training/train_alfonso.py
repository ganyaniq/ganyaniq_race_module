# train_alfonso.py
from model_train import train_model
import logging

def start_training():
    logging.info("Alfonso AI eğitimi başlatılıyor...")
    try:
        train_model()
        logging.info("Alfonso AI eğitimi başarıyla tamamlandı.")
    except Exception as e:
        logging.error(f"Eğitim sırasında hata oluştu: {e}")

if __name__ == "__main__":
    start_training()
