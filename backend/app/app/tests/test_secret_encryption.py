"""Tests for the Numerai API secret encryption shim."""

import unittest

from app.core import crypto
from app.core.config import settings
from app.models.user import User


def _make_user():
    return User(id=1, numerai_api_key_secret_stored=None)


class TestSecretEncryption(unittest.TestCase):
    def setUp(self):
        self.key = crypto.Fernet.generate_key().decode()
        settings.DATA_ENCRYPTION_KEY = self.key

    def tearDown(self):
        settings.DATA_ENCRYPTION_KEY = None

    def test_write_encrypts(self):
        user = _make_user()
        user.numerai_api_key_secret = "hunter2"
        self.assertTrue(user.numerai_api_key_secret_stored.startswith("gAAA"))
        self.assertNotEqual(user.numerai_api_key_secret_stored, "hunter2")

    def test_read_decrypts(self):
        user = _make_user()
        user.numerai_api_key_secret_stored = crypto.encrypt_secret("new")
        self.assertEqual(user.numerai_api_key_secret, "new")

    def test_read_none(self):
        user = _make_user()
        self.assertIsNone(user.numerai_api_key_secret)

    def test_read_bad_ciphertext_raises(self):
        from cryptography.fernet import InvalidToken

        user = _make_user()
        user.numerai_api_key_secret_stored = "gAAAnotarealtoken"
        with self.assertRaises(InvalidToken):
            user.numerai_api_key_secret

    def test_plaintext_fails_closed_with_key(self):
        from cryptography.fernet import InvalidToken

        user = _make_user()
        user.numerai_api_key_secret_stored = "plain"
        with self.assertRaises(InvalidToken):
            user.numerai_api_key_secret

    def test_dev_mode_without_key(self):
        settings.DATA_ENCRYPTION_KEY = None
        user = _make_user()
        user.numerai_api_key_secret = "hunter2"
        self.assertEqual(user.numerai_api_key_secret_stored, "hunter2")
        self.assertEqual(user.numerai_api_key_secret, "hunter2")

    def test_empty_string_roundtrip(self):
        user = _make_user()
        user.numerai_api_key_secret = ""
        self.assertTrue(user.numerai_api_key_secret_stored.startswith("gAAA"))
        self.assertEqual(user.numerai_api_key_secret, "")

    def test_clear_with_none(self):
        user = _make_user()
        user.numerai_api_key_secret = "hunter2"
        user.numerai_api_key_secret = None
        self.assertIsNone(user.numerai_api_key_secret_stored)
        self.assertIsNone(user.numerai_api_key_secret)

    def test_encode_helper_exposes_secret(self):
        from app.utils import encode_user_for_numerai

        user = _make_user()
        user.numerai_api_key_secret_stored = crypto.encrypt_secret("secret")
        user.username = "testuser"
        encoded = encode_user_for_numerai(user)
        self.assertEqual(encoded["numerai_api_key_secret"], "secret")
        self.assertNotIn("numerai_api_key_secret_stored", encoded)


if __name__ == "__main__":
    unittest.main()
