"""
Configuration settings for the Energy Dashboard Flask application.
"""

import os

class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///robots.db")  # Default to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1']
    TESTING = os.environ.get('TESTING', 'False').lower() in ['true', '1']
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///site.db')  # Default to SQLite

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI')  # Ensure the database is set

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///dev.db')  # Use a different DB for development

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///test.db')  # Use a different DB for testing

# You can add more configurations as necessary
