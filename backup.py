import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "ulugbek_ai.db"
BACKUP_DIR = "backups"


def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    data = {
        "created_at": datetime.utcnow().isoformat(),
        "users": [dict(row) for row in connection.execute("SELECT * FROM users")],
        "chats": [dict(row) for row in connection.execute("SELECT * FROM chats")],
        "knowledge": [dict(row) for row in connection.execute("SELECT * FROM knowledge")]
    }

    connection.close()

    filename = datetime.utcnow().strftime("backup_%Y%m%d_%H%M%S.json")
    path = os.path.join(BACKUP_DIR, filename)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return path


if __name__ == "__main__":
    print("Zaxira yaratildi:", create_backup())
