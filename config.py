import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///projects.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = {
        'en': 'English',
        'ja': '日本語',
        'es': 'Español',
        'zh': '中文'
    }
    BABEL_DEFAULT_LOCALE = 'en'
