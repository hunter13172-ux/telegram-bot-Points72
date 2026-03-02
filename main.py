import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
FILE = "database.json"


# ==========================
# 📦 تحميل البيانات
# ==========================
def load_db():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_db(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


db = load_db()


# ==========================
# ➕ إضافة نقاط
# ==========================
async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        return await update.message.reply_text("استخدم: /give اسم عدد")

    user = context.args[0]

    try:
        amount = int(context.args[1])
    except:
        return await update.message.reply_text("❌ الرقم غير صحيح")

    db[user] = db.get(user, 0) + amount
    save_db(db)

    await update.message.reply_text(f"✅ تم إعطاء {amount} نقطة لـ {user}")


# ==========================
# ➖ سحب نقاط
# ==========================
async def take(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        return await update.message.reply_text("استخدم: /take اسم عدد")

    user = context.args[0]

    try:
        amount = int(context.args[1])
    except:
        return await update.message.reply_text("❌ الرقم غير صحيح")

    db[user] = db.get(user, 0) - amount
    save_db(db)

    await update.message.reply_text(f"❌ تم سحب {amount} نقطة من {user}")


# ==========================
# 🏆 عرض الترتيب
# ==========================
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not db:
        return await update.message.reply_text("❌ لا توجد بيانات")

    sorted_data = sorted(db.items(), key=lambda x: x[1], reverse=True)[:10]

    text = "🏅 أفضل 10:\n\n"
    for i, (name, points) in enumerate(sorted_data, 1):
        text += f"{i}. {name} ➜ {points}\n"

    await update.message.reply_text(text)


# ==========================
# 🚀 تشغيل البوت
# ==========================
async def main():
    if not TOKEN:
        raise ValueError("TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("give", give))
    app.add_handler(CommandHandler("take", take))
    app.add_handler(CommandHandler("top", top))

    print("🚀 Bot Running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
