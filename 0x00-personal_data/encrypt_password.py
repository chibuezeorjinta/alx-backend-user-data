#!/usr/bin/env python3
"""Password protection functions"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypt the provided string"""
    encode_str = password.encode()
    gen_salt = bcrypt.gensalt()
    out_encrypted = bcrypt.hashpw(encode_str, gen_salt)
    return out_encrypted


def is_valid(hashed_password: bytes, password: str) -> bool:
    """use bcrypt to check if password has been hashed before"""
    encode_str = password.encode()
    if bcrypt.checkpw(encode_str, hashed_password):
        return True
    return False
