import pytest
import string
from core.encryption import derive_key, encrypt_data, decrypt_data
from core.password_generator import generate_password
from core.strength_checker import check_strength

def test_encryption():
    key = derive_key("testpassword", b"salt1234567890123456")
    data = "test data"
    enc = encrypt_data(data, key)
    dec = decrypt_data(enc, key)
    assert dec == data

def test_password_generator():
    pwd = generate_password(10, True, True, True, True)
    assert len(pwd) == 10
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in string.punctuation for c in pwd)

def test_strength_checker():
    weak = check_strength("123")
    medium = check_strength("password123")
    strong = check_strength("P@ssw0rd123!")
    assert weak == "weak"
    assert medium == "medium"
    assert strong == "strong"