pip uninstall telegram  # якщо встановлений неправильний пакет
pip install python-telegram-bot --upgrade
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, ConversationHandler, filters
