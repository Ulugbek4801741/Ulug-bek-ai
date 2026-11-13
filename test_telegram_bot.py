import os
import tempfile
import unittest
from unittest.mock import patch

import telegram_bot


class TelegramBotTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        telegram_bot.DB_PATH = os.path.join(self.tempdir.name, "test.sqlite3")
        telegram_bot.BOT_TOKEN = "test-token"
        telegram_bot.WEBHOOK_SECRET = "test-webhook-secret"
        telegram_bot.create_telegram_blueprint(lambda prompt, system: ("Javob", "test"))
        self.client = telegram_bot.telegram_bp.test_client()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_rejects_invalid_webhook_secret(self):
        response = self.client.post(
            "/telegram/webhook",
            json={"message": {"chat": {"id": 1}, "text": "/start"}},
            headers={"X-Telegram-Bot-Api-Secret-Token": "wrong"},
        )
        self.assertEqual(response.status_code, 401)

    @patch("telegram_bot._telegram")
    def test_start_command_returns_ok_and_sends_menu(self, send):
        response = self.client.post(
            "/telegram/webhook",
            json={"message": {"chat": {"id": 123}, "text": "/start"}},
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-webhook-secret"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"ok": True})
        send.assert_called_once()
        self.assertEqual(send.call_args.args[0], "sendMessage")

    @patch("telegram_bot._telegram")
    def test_order_mode_persists_customer_request(self, send):
        headers = {"X-Telegram-Bot-Api-Secret-Token": "test-webhook-secret"}
        self.client.post(
            "/telegram/webhook",
            json={"callback_query": {
                "id": "cb1",
                "data": "mode:order",
                "message": {"chat": {"id": 456}},
            }},
            headers=headers,
        )
        self.client.post(
            "/telegram/webhook",
            json={"message": {
                "chat": {"id": 456},
                "from": {"id": 456, "username": "buyer"},
                "text": "Menga internet do‘kon kerak",
            }},
            headers=headers,
        )
        connection = telegram_bot._db()
        row = connection.execute(
            "SELECT details, status FROM telegram_orders"
        ).fetchone()
        connection.close()
        self.assertEqual(row["details"], "Menga internet do‘kon kerak")
        self.assertEqual(row["status"], "new")


if __name__ == "__main__":
    unittest.main()
