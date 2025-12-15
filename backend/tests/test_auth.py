"""
Unit tests for the authentication module.
"""

import pytest
from ..app.core.auth import verify_password, get_password_hash

def test_password_hashing():
    """Test that password hashing and verification work correctly."""
    password = "test_password_123"
    hashed = get_password_hash(password)

    # Verify the password matches the hash
    assert verify_password(password, hashed) == True

    # Verify a wrong password doesn't match
    assert verify_password("wrong_password", hashed) == False

def test_password_hash_different():
    """Test that hashing the same password produces different hashes (due to salt)."""
    password = "test_password_123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Bcrypt (used by passlib) includes a salt, so hashes should be different
    assert hash1 != hash2

    # But both should verify against the original password
    assert verify_password(password, hash1) == True
    assert verify_password(password, hash2) == True

def test_empty_password():
    """Test behavior with empty passwords."""
    empty_hash = get_password_hash("")
    assert verify_password("", empty_hash) == True
    assert verify_password("non_empty", empty_hash) == False

def test_long_password():
    """Test behavior with very long passwords."""
    long_password = "a" * 1000  # 1000 character password
    hashed = get_password_hash(long_password)
    assert verify_password(long_password, hashed) == True
    assert verify_password("different", hashed) == False