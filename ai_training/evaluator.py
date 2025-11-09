# 📁 MODÜL: evaluator.py
# 🧾 AÇIKLAMA: Alfonso'nun tahmin sonuçlarının doğruluğunu ölçer, metrik raporlar üretir

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd


def degerlendir_model(y_true, y_pred):
    """
    Gerçek değerler ve tahminlere göre performans ölçer.
    :param y_true: Gerçek etiketler
    :param y_pred: Modelin tahmin ettiği etiketler
    :return: Performans metrikleri sözlüğü
    """
    try:
        acc = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        report = classification_report(y_true, y_pred, output_dict=True)

        return {
            "accuracy": acc,
            "confusion_matrix": cm.tolist(),
            "classification_report": report
        }
    except Exception as e:
        return {"hata": f"Değerlendirme yapılamadı: {e}"}


# Örnek test:
# y_true = [1, 0, 1, 1, 0]
# y_pred = [1, 0, 0, 1, 0]
# print(degerlendir_model(y_true, y_pred))
