import unittest
from unittest.mock import Mock, patch

import agent


class GoogleLoginSecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = agent.app.test_client()
        self.original_client_id = agent.GOOGLE_CLIENT_ID
        agent.GOOGLE_CLIENT_ID = "test-google-client.apps.googleusercontent.com"

    def tearDown(self):
        agent.GOOGLE_CLIENT_ID = self.original_client_id

    @patch("agent.requests.get")
    def test_login_accepts_verified_token_with_matching_audience(self, get):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "iss": "https://accounts.google.com",
            "aud": agent.GOOGLE_CLIENT_ID,
            "email_verified": "true",
            "sub": "test-subject-123",
            "name": "Test User",
            "email": "test@example.com",
            "picture": "",
        }
        get.return_value = response

        result = self.client.post(
            "/api/login",
            json={"credential": "signed.jwt.token"},
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.get_json()["user"]["google_id"], "test-subject-123")
        get.assert_called_once()

    @patch("agent.requests.get")
    def test_login_rejects_token_for_different_audience(self, get):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "iss": "accounts.google.com",
            "aud": "another-client-id",
            "email_verified": True,
            "sub": "attacker-subject",
            "email": "attacker@example.com",
        }
        get.return_value = response

        result = self.client.post(
            "/api/login",
            json={"credential": "signed.jwt.token"},
        )

        self.assertEqual(result.status_code, 401)
        self.assertIn("boshqa ilova", result.get_json()["error"])

    def test_login_rejects_missing_credential(self):
        result = self.client.post("/api/login", json={})
        self.assertEqual(result.status_code, 400)


if __name__ == "__main__":
    unittest.main()
