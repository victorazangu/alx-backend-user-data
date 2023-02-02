#!/usr/bin/env python3
"""
encrypt_password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash_password function
    """
    password = bytes(password, 'utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    is_valid function
    """
    return bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password)
