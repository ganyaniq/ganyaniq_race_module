import shutil
import datetime
import os

def backup_database(db_path="ganyaniq.db", backup_dir="backups/"):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"ganyaniq_backup_{timestamp}.db")
    shutil.copy2(db_path, backup_file)
    print(f"Backup oluşturuldu: {backup_file}")

if __name__ == "__main__":
    backup_database()
