import unittest
from unittest.mock import Mock, patch

import agent


class GeminiRequestTests(unittest.TestCase):
    @patch("agent.requests.post")
    def test_api_key_is_sent_in_header_not_url(self, post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "candidates": [{
                "content": {"parts": [{"text": "Salom"}, {"text": "dunyo"}]}
            }]
        }
        post.return_value = response

        answer = agent.ask_gemini("Salom", "O‘zbekcha javob ber", "TEST_ONLY_SECRET")

        self.assertEqual(answer, "Salom\\ndunyo")
        args, kwargs = post.call_args
        self.assertNotIn("TEST_ONLY_SECRET", args[0])
        self.assertNotIn("?", args[0])
        self.assertEqual(kwargs["headers"]["X-goog-api-key"], "TEST_ONLY_SECRET")
        self.assertEqual(kwargs["json"]["contents"][0]["parts"][0]["text"], "Salom")

    @patch("agent.requests.post")
    def test_non_200_response_returns_none(self, post):
        response = Mock()
        response.status_code = 401
        post.return_value = response

        self.assertIsNone(agent.ask_gemini("test", "system", "TEST_ONLY_SECRET"))

    @patch("agent.requests.post")
    def test_empty_candidate_returns_none(self, post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"candidates": []}
        post.return_value = response

        self.assertIsNone(agent.ask_gemini("test", "system", "TEST_ONLY_SECRET"))


if __name__ == "__main__":
    unittest.main()
