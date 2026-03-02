import json
import os
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
            with open(FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # إذا الملف تالف نعيد قاموس فارغ بدل كسر البوت
            return {}
        except Exception:
            return {}
    return {}


def save_db(data):
    # احفظ بالترميز UTF-8 عشان العربي يطلع مضبوط
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


db = load_db()


# ➕ إضافة نقاط
async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        return await update.message.reply_text("استخدم: /give اسم عدد")

    user = context.args[0]

    try:
        amount = int(context.args[1])
    except ValueError:
        return await update.message.reply_text("❌ الرقم غير صحيح")

    db[user] = db.get(user, 0) + amount
    save_db(db)

    await update.message.reply_text(f"✅ تم إعطاء {amount} نقطة لـ {user}")


# ➖ سحب نقاط
async def take(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        return await update.message.reply_text("استخدم: /take اسم عدد")

    user = context.args[0]

    try:
        amount = int(context.args[1])
    except ValueError:
        return await update.message.reply_text("❌ الرقم غير صحيح")

    db[user] = db.get(user, 0) - amount
    save_db(db)

    await update.message.reply_text(f"❌ تم سحب {amount} نقطة من {user}")


# 📄 رصيد مستخدم (اختياري مفيد)
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نجرب اسم من الوسيط أو اسم المستخدم اللي أرسل الأمر
    if context.args:
        user = context.args[0]
    else:
        user = update.effective_user.username or str(update.effective_user.id)

    points = db.get(user, 0)
    await update.message.reply_text(f"🔸 رصيد {user}: {points} نقطة")


# 🏆 ترتيب
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not db:
        return await update.message.reply_text("❌ لا توجد بيانات")

    sorted_data = sorted(db.items(), key=lambda x: x[1], reverse=True)[:10]

    text = "🏅 أفضل 10:\n\n"
    for i, (name, points) in enumerate(sorted_data, 1):
        text += f"{i}. {name} ➜ {points}\n"

    await update.message.reply_text(text)


# 🚀 تشغيل البوت
def main():
    if not TOKEN:
        raise ValueError("TOKEN غير موجود. عيّن متغير البيئة TOKEN قبل التشغيل")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("give", give))
    app.add_handler(CommandHandler("take", take))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("balance", balance))  # أمر اختياري

    print("🚀 Bot Running...")
    app.run_polling()


if name == "main":
    main()
