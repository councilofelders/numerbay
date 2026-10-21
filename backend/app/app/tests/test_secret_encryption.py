"""Tests for the Numerai API secret encryption shim."""

import unittest

from app.core import crypto
from app.core.config import settings
from app.models.user import User


def _make_user():
    user = User.__new__(User)
    user.numerai_api_key_secret_stored = None
    user.numerai_api_key_secret_backup = None
    user.id = 1
    return user


class TestSecretEncryption(unittest.TestCase):
    def setUp(self):
        self.key = crypto.Fernet.generate_key().decode()
        settings.DATA_ENCRYPTION_KEY = self.key

    def tearDown(self):
        settings.DATA_ENCRYPTION_KEY = None

    def test_write_encrypts_and_mirrors(self):
        user = _make_user()
        user.numerai_api_key_secret = "hunter2"
        self.assertIsNotNone(user.numerai_api_key_secret_stored)
        self.assertTrue(user.numerai_api_key_secret_stored.startswith("gAAA"))
        self.assertNotEqual(user.numerai_api_key_secret_stored, "hunter2")
        self.assertEqual(user.numerai_api_key_secret_backup, "hunter2")

    def test_read_decrypts_encrypted(self):
        user = _make_user()
        user.numerai_api_key_secret_stored = crypto.encrypt_secret("new")
        user.numerai_api_key_secret_backup = "old"
        self.assertEqual(user.numerai_api_key_secret, "new")

    def test_read_plaintext_passthrough(self):
        user = _make_user()
        user.numerai_api_key_secret_stored = "plain"
        user.numerai_api_key_secret_backup = "plain"
        self.assertEqual(user.numerai_api_key_secret, "plain")

    def test_read_none(self):
        user = _make_user()
        self.assertIsNone(user.numerai_api_key_secret)

    def test_write_without_key_stores_plaintext(self):
        settings.DATA_ENCRYPTION_KEY = None
        user = _make_user()
        user.numerai_api_key_secret = "hunter2"
        self.assertEqual(user.numerai_api_key_secret_stored, "hunter2")
        self.assertEqual(user.numerai_api_key_secret_backup, "hunter2")

    def test_read_bad_ciphertext_falls_back(self):
        user = _make_user()
        user.numerai_api_key_secret_stored = "gAAAnotarealtoken"
        user.numerai_api_key_secret_backup = "backup_value"
        self.assertEqual(user.numerai_api_key_secret, "backup_value")

    def test_encode_helper_exposes_secret(self):
        from app.utils import encode_user_for_numerai

        user = _make_user()
        user.numerai_api_key_secret_stored = crypto.encrypt_secret("secret")
        user.numerai_api_key_secret_backup = "secret"
        user.username = "testuser"
        encoded = encode_user_for_numerai(user)
        self.assertEqual(encoded["numerai_api_key_secret"], "secret")
        self.assertNotIn("numerai_api_key_secret_stored", encoded)
        self.assertNotIn("numerai_api_key_secret_backup", encoded)


if __name__ == "__main__":
    unittest.main()
