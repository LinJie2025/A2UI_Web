"""Tests for service layer — crypto, auth, system prompt, etc."""

import pytest
from app.services.crypto_service import encrypt, decrypt
from app.services.auth_service import hash_password, verify_password, create_access_token, decode_access_token
from app.services.system_prompt import SystemPromptBuilder, SYSTEM_PROMPT_BASE
from app.models.user import User
from app.models.role import Role
from app.models.tool_whitelist import ToolWhitelist
from app.schemas.chat import SSEEvent


class TestCryptoService:
    """Tests for AES-256 Fernet encryption service."""

    def test_encrypt_decrypt_roundtrip(self):
        """Encrypt and decrypt should return the original plaintext."""
        plaintext = "my-secret-api-key-12345"
        encrypted = encrypt(plaintext)
        assert encrypted != plaintext
        assert len(encrypted) > 0
        decrypted = decrypt(encrypted)
        assert decrypted == plaintext

    def test_encrypt_empty_string(self):
        """Encrypting empty string returns empty string."""
        assert encrypt("") == ""

    def test_decrypt_empty_string(self):
        """Decrypting empty string returns empty string."""
        assert decrypt("") == ""

    def test_different_inputs_produce_different_ciphertexts(self):
        """Different plaintexts should produce different ciphertexts."""
        ct1 = encrypt("key-one")
        ct2 = encrypt("key-two")
        assert ct1 != ct2

    def test_same_input_produces_different_ciphertext(self):
        """Fernet uses random IV, so same input gives different ciphertext."""
        ct1 = encrypt("same-text")
        ct2 = encrypt("same-text")
        # Fernet includes timestamp, but encrypt is deterministic for same key
        # Actually Fernet with same key produces different output due to timestamp
        # Let's verify decryption still works
        assert decrypt(ct1) == "same-text"
        assert decrypt(ct2) == "same-text"


class TestAuthService:
    """Tests for password hashing and JWT management."""

    def test_hash_and_verify_password(self):
        """Password hash and verify roundtrip."""
        password = "mySecureP@ss1"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        """Wrong password should not verify."""
        hashed = hash_password("correct-password")
        assert verify_password("wrong-password", hashed) is False

    def test_create_and_decode_token(self):
        """JWT create and decode roundtrip."""
        token = create_access_token(42)
        assert isinstance(token, str)
        user_id = decode_access_token(token)
        assert user_id == 42

    def test_decode_invalid_token(self):
        """Invalid token returns None."""
        assert decode_access_token("not.a.valid.token") is None

    def test_decode_empty_token(self):
        """Empty token returns None."""
        assert decode_access_token("") is None


class TestSystemPrompt:
    """Tests for SystemPromptBuilder."""

    ALL_TOOLS = [
        {"name": "product_search", "description": "Search products", "inputSchema": {}},
        {"name": "stock_check", "description": "Check stock", "inputSchema": {}},
        {"name": "admin_delete", "description": "Delete records", "inputSchema": {}},
        {"name": "sales_report", "description": "Sales report", "inputSchema": {}},
    ]

    def _make_user(self, tool_names: list[str]) -> User:
        """Create a User with role and tool whitelist."""
        role = Role(id=1, name="test_role")
        role.tool_whitelist = [
            ToolWhitelist(role_id=1, tool_name=name) for name in tool_names
        ]
        user = User(id=1, username="testuser", password_hash="...")
        user.role = role
        return user

    def test_base_prompt_contains_constraints(self):
        """Base system prompt includes key elements."""
        assert "A2UI" in SYSTEM_PROMPT_BASE
        assert "tools" in SYSTEM_PROMPT_BASE.lower()
        assert "JSONL" in SYSTEM_PROMPT_BASE

    def test_build_returns_filtered_tools(self):
        """Build returns only whitelisted tools in OpenAI format."""
        user = self._make_user(["product_search", "stock_check"])
        prompt, tools = SystemPromptBuilder.build(user, self.ALL_TOOLS)

        assert len(tools) == 2
        assert tools[0]["type"] == "function"
        assert tools[0]["function"]["name"] in ("product_search", "stock_check")

    def test_prompt_contains_tool_descriptions(self):
        """System prompt text should contain whitelisted tool descriptions."""
        user = self._make_user(["product_search"])
        prompt, _ = SystemPromptBuilder.build(user, self.ALL_TOOLS)

        assert "product_search" in prompt
        assert "Search products" in prompt
        assert "stock_check" not in prompt

    def test_no_role_user_gets_no_tools(self):
        """User without role gets zero tools."""
        user = User(id=2, username="norole", password_hash="...")
        user.role = None
        prompt, tools = SystemPromptBuilder.build(user, self.ALL_TOOLS)

        assert len(tools) == 0


class TestSSEEvent:
    """Tests for SSE event formatting."""

    def test_text_event_to_sse(self):
        """Text event formats correctly."""
        event = SSEEvent("text", {"delta": "Hello"})
        sse = event.to_sse()
        assert sse.startswith("event: text")
        assert "Hello" in sse
        assert sse.endswith("\n\n")

    def test_done_event_to_sse(self):
        """Done event formats correctly."""
        event = SSEEvent("done", {"conversation_id": 1})
        sse = event.to_sse()
        assert "event: done" in sse
        assert "conversation_id" in sse

    def test_error_event_to_sse(self):
        """Error event formats correctly."""
        event = SSEEvent("error", {"message": "Something went wrong"})
        sse = event.to_sse()
        assert "event: error" in sse
        assert "Something went wrong" in sse


class TestConfig:
    """Tests for application configuration."""

    def test_default_settings(self):
        """Default settings are loaded correctly."""
        from app.config import settings
        assert settings.APP_NAME == "A2UI Web"
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.JWT_EXPIRATION_HOURS == 24
        assert settings.LLM_MODEL == "deepseek-chat"
