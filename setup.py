"""
Quiz Bot Setup
Aiogram 3.22 uchun Quiz Bot
"""

from setuptools import setup, find_packages

setup(
    name="quiz-bot",
    version="1.0.0",
    description="Telegram Quiz Bot with aiogram 3.22",
    author="Quiz Bot Team",
    packages=find_packages(),
    install_requires=[
        "aiogram==3.22.0",
        "aiohttp==3.9.1",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "quiz-bot=main:main",
        ],
    },
)
