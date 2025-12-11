import os

class Config:
    # Secret key used for sessions and CSRF protection
    SECRET_KEY = "my_super_secret_key_123456789"

    # Security for cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False 
    SESSION_COOKIE_SAMESITE = "Lax"
