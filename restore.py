import sqlite3
import json
import sys

DB_PATH = "ulugbek_ai.db"


def restore_backup(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    connection = sqlite3.connect(DB_PATH)

    for user in data.get("users", []):
        connection.execute(
            """
            INSERT OR IGNORE INTO users
            (google_id, name, email, picture, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user.get("google_id"),
                user.get("name"),
                user.get("email"),
                user.get("picture"),
                user.get("created_at")
            )
        )

    for chat in data.get("chats", []):
        connection.execute(
            """
            INSERT INTO chats
            (user_email, question, answer, rating, provider, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                chat.get("user_email"),
                chat.get("question"),
                chat.get("answer"),
                chat.get("rating"),
                chat.get("provider"),
                chat.get("created_at")
            )
        )

    for item in data.get("knowledge", []):
        connection.execute(
            """
            INSERT INTO knowledge
            (title, content, active, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                item.get("title"),
                item.get("content"),
                item.get("active", 1),
                item.get("created_at")
            )
        )

    connection.commit()
    connection.close()

    print("Ma’lumotlar tiklandi:", path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Foydalanish: python restore.py backups/backup_fayli.json")
    else:
        restore_backup(sys.argv[1])
