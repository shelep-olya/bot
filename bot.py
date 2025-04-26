import telegram
import telegram.ext
from db import *

TOKEN = "7867992980:AAGGkKZoV5ClpzQ65UBJlhjAOgJy4urDhYk"

CHOOSING, ADDING_DAY, ADDING_TIME, ADDING_TITLE, ASK_DAY = range(5)
user_entry = {}

keyboard = [
    ["Розклад на весь тиждень"],
    ["Розклад на конкретний день"],
    ["Відредагувати розклад"],
    ["Додати подію"]
]
reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


async def start(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Що ти хочеш зробити?", reply_markup=reply_markup)
    return CHOOSING


async def handle_choice(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "Розклад на весь тиждень":
        schedule = get_schedule()
        if schedule:
            msg = "\n".join([f"{r[0]}. {r[1]}, {r[2]} — {r[3]}" for r in schedule])
        else:
            msg = "Немає записів у розкладі."
        await update.message.reply_text(msg)
    elif choice == "Розклад на конкретний день":
        await update.message.reply_text("Введи день тижня:")
        return ASK_DAY
    elif choice == "Додати подію":
        await update.message.reply_text("Введи день тижня:")
        return ADDING_DAY
    elif choice == "Відредагувати розклад":
        await update.message.reply_text("Редагування в розробці 😉")
    return telegram.ext.ConversationHandler.END


async def handle_day_query(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    day = update.message.text
    schedule = get_schedule_by_day(day)
    if schedule:
        msg = "\n".join([f"{r[0]}. {r[2]} — {r[3]}" for r in schedule])
    else:
        msg = f"Немає подій на {day}."
    await update.message.reply_text(msg)
    return telegram.ext.ConversationHandler.END


async def add_entry_day(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    user_entry["day"] = update.message.text
    await update.message.reply_text("Введи час події (наприклад, 14:00):")
    return ADDING_TIME


async def add_entry_time(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    user_entry["time"] = update.message.text
    await update.message.reply_text("Введи назву події:")
    return ADDING_TITLE


async def add_entry_title(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    user_entry["title"] = update.message.text
    add_schedule_entry(user_entry["day"], user_entry["time"], user_entry["title"])
    await update.message.reply_text("Запис успішно додано ✅")
    user_entry.clear()
    return telegram.ext.ConversationHandler.END

if __name__ == "__main__":
    init_db()

    app = telegram.ext.ApplicationBuilder().token(TOKEN).build()

    main_handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, handle_choice)], 
        states={
            CHOOSING: [telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, handle_choice)],
            ASK_DAY: [telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, handle_day_query)],
            ADDING_DAY: [telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, add_entry_day)],
            ADDING_TIME: [telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, add_entry_time)],
            ADDING_TITLE: [telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, add_entry_title)],
         
        },
        fallbacks=[]
    )

app.add_handler(main_handler)
app.run_polling()
