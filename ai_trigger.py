import random

def trigger_ai(data=None):
    atlar = data.get("atlar", []) if data else ["At1", "At2", "At3", "At4"]
    if not atlar:
        return {"status": "error", "message": "Hiç at verilmedi."}
    tahmin = random.choice(atlar)
    return {
        "status": "ok",
        "message": f"Alfonso'nun favori atı: {tahmin}",
        "tarihce": sorted(random.sample(atlar, min(3, len(atlar))))
    }
