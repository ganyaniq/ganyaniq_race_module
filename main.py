import threading
import time
from kategoriler import deklareler  # Diğer modüller eklenecek

def run_module(module_func, interval_seconds):
    def wrapper():
        while True:
            try:
                module_func.main()
            except Exception as e:
                print(f"Error in {module_func.__name__}: {e}")
            time.sleep(interval_seconds)
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    modules = [
        (deklareler, 300),  # 5 dakikada bir çalıştır
        # Diğer modüller buraya eklenecek
    ]

    threads = []
    for mod, interval in modules:
        t = run_module(mod, interval)
        threads.append(t)

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Program durduruldu.")
