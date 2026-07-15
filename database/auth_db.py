"""
SQLite database service for CLARIO authentication.

Handles user registration, password hashing (PBKDF2-SHA256), and credentials verification.
"""

import sqlite3
import hashlib
import os
from pathlib import Path
from typing import Optional, Dict, Tuple

DB_PATH = Path(__file__).resolve().parent / "auth_db.sqlite"


def get_connection():
    """Establish a connection to the SQLite authentication database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database tables if they do not exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt.hex() + ":" + key.hex()


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a password against its stored hash."""
    try:
        salt_hex, key_hex = stored_password.split(":")
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac(
            "sha256", provided_password.encode("utf-8"), salt, 100000
        )
        return key == new_key
    except Exception:
        return False


def create_user(email: str, password: str, name: str) -> Tuple[bool, str]:
    """
    Register a new user in the system.

    Returns:
        (bool, str): (Success state, message/error details).
    """
    init_db()  # Ensure DB is ready
    email_clean = email.strip().lower()
    name_clean = name.strip()

    if not email_clean or not password or not name_clean:
        return False, "All fields are required."

    pw_hash = hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
                (email_clean, pw_hash, name_clean),
            )
            conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def verify_user(email: str, password: str) -> Optional[Dict]:
    """
    Verify user credentials.

    Returns:
        Optional[Dict]: Dict containing user info (email, name) if successful, None otherwise.
    """
    init_db()  # Ensure DB is ready
    email_clean = email.strip().lower()

    if not email_clean or not password:
        return None

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT email, password_hash, name FROM users WHERE email = ?",
                (email_clean,),
            )
            row = cursor.fetchone()

            if row and verify_password(row["password_hash"], password):
                return {"email": row["email"], "name": row["name"]}
    except Exception:
        pass
    return None
