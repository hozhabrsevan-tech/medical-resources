
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN, ADMIN_ID

from database import (
    create_tables,
    show_resources,
    get_resource,
    add_resource
)

from keyboards import main_keyboard, admin_keyboard, admin_category_keyboard, admin_type_keyboard


# ==================================================
# Logging
# ==================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 منابع درسی\n\n"
        "یک بخش را انتخاب کن:",
        reply_markup=main_keyboard()
    )


# پنل مدیریت
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ شما دسترسی مدیریت ندارید."
        )
        return

    await update.message.reply_text(
        "🔐 پنل مدیریت\n\n"
        "یکی از گزینه‌ها را انتخاب کن:",
        reply_markup=admin_keyboard()
    )



    
async def go_home(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        "📚 منابع درسی\n\n"
        "یک بخش را انتخاب کن:",

        reply_markup=main_keyboard()
    )


# ==================================================
# نمایش منابع یک دسته
# ==================================================

async def show_category(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # مثال:
    #
    # category_anatomy
    #
    # تبدیل می‌شود به:
    #
    # anatomy

    category = query.data.replace(
        "category_",
        ""
    )

    resources = show_resources(category)

    keyboard = []

    # اگر منبعی وجود نداشت

    if not resources:

        keyboard.append([

            InlineKeyboardButton(
                "❌ هنوز منبعی وجود ندارد",
                callback_data="nothing"
            )

        ])

    else:

        for resource_id, title, resource_type in resources:

            keyboard.append([

                InlineKeyboardButton(

                    title,

                    callback_data=(
                        f"resource_{resource_id}"
                    )
                )

            ])

    # دکمه بازگشت

    keyboard.append([

        InlineKeyboardButton(
            "⬅️ بازگشت",
            callback_data="home"
        )

    ])

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await query.edit_message_text(

        f"📚 منابع {category}\n\n"
        "یک منبع را انتخاب کن:",

        reply_markup=reply_markup
    )


# ==================================================
# ارسال منبع
# ==================================================

async def send_resource(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # مثال:
    #
    # resource_5
    #
    # تبدیل می‌شود به:
    #
    # 5

    resource_id = int(
        query.data.replace(
            "resource_",
            ""
        )
    )

    resource = get_resource(resource_id)

    # اگر منبع پیدا نشد

    if resource is None:

        await query.message.reply_text(
            "❌ این منبع پیدا نشد."
        )

        return

    (
        resource_id,
        title,
        category,
        resource_type,
        file_id,
        link,
        description
    ) = resource


    # -------------------------
    # PDF
    # -------------------------

    if resource_type == "pdf":

        await query.message.reply_document(

            document=file_id,

            caption=(
                f"📖 {title}\n\n"
                f"{description or ''}"
            )
        )

    elif resource_type == "video":
        await query.message.reply_video(
        video=file_id,
        caption=f"🎥 {title}\n\n{description or ''}"
    )

    elif resource_type == "voice":
        await query.message.reply_voice(
        voice=file_id,
        caption=f"🎙 {title}\n\n{description or ''}"
    )

    elif resource_type == "audio":
        await query.message.reply_audio(
        audio=file_id,
        caption=f"🔊 {title}\n\n{description or ''}"
    )
    # -------------------------
    # نمونه سوال
    # -------------------------

    elif resource_type == "questions":

        await query.message.reply_document(

            document=file_id,

            caption=f"📝 {title}"
        )


    # -------------------------
    # لینک
    # -------------------------

    elif resource_type == "link":

        await query.message.reply_text(

            f"🔗 {title}\n\n"
            f"{link}"
        )


    # -------------------------
    # ویدئو
    # -------------------------

    elif resource_type == "video":

        await query.message.reply_text(

            f"🎥 {title}\n\n"
            f"{link}"
        )


# ==================================================
# گرفتن File ID
# ==================================================

async def get_file_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # فقط Admin اجازه دارد

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ شما دسترسی مدیریت ندارید."
        )

        return


    # گرفتن اطلاعات فایل

    document = update.message.document

    file_id = document.file_id


    # نمایش File ID

    await update.message.reply_text(

        "📄 File ID:\n\n"
        f"{file_id}"
    )

    logger.info(
        "Admin uploaded a file. file_id=%s",
        file_id
    )

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your ID: {update.effective_user.id}"
    )
# ==================================================
# Callback Handler
# ==================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "home":
        await go_home(update, context)

    elif data.startswith("category_"):
        await show_category(update, context)

    elif data.startswith("resource_"):
        await send_resource(update, context)

    elif data == "admin_add":
        if update.effective_user.id != ADMIN_ID:
            await query.answer("دسترسی ندارید.", show_alert=True)
            return

        await query.answer()
        context.user_data["adding_resource"] = True
        context.user_data["add_step"] = "category"

        await query.message.reply_text(
            "📚 دسته‌بندی منبع رو انتخاب کن:",
            reply_markup=admin_category_keyboard()
        )

    elif data.startswith("addcat_"):
        if update.effective_user.id != ADMIN_ID:
            await query.answer("دسترسی ندارید.", show_alert=True)
            return

        context.user_data["category"] = data.replace("addcat_", "")
        context.user_data["add_step"] = "type"

        await query.answer()
        await query.message.reply_text(
            "📌 نوع منبع رو انتخاب کن:",
            reply_markup=admin_type_keyboard()
        )

    elif data.startswith("addtype_"):
        if update.effective_user.id != ADMIN_ID:
            await query.answer("دسترسی ندارید.", show_alert=True)
            return

        context.user_data["resource_type"] = data.replace("addtype_", "")
        context.user_data["add_step"] = "title"

        await query.answer()
        await query.message.reply_text("✏️ عنوان منبع رو بفرست:")

    elif data in ["admin_list", "admin_delete"]:
        await query.answer(
            "این بخش هنوز پیاده‌سازی نشده است.",
            show_alert=True
        )

    elif data in ["questions", "search", "favorites", "nothing"]:
        await query.answer(
            "این بخش را هنوز نساخته‌ایم 🙂",
            show_alert=True
        )       
    
async def admin_add_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.user_data.get("adding_resource"):
        return

    step = context.user_data.get("add_step")
    message = update.message

    if step == "title":
        context.user_data["title"] = message.text
        context.user_data["add_step"] = "description"

        await message.reply_text(
            "📝 توضیحات منبع رو بفرست.\n"
            "اگر توضیحی نداری، فقط یک خط تیره (-) بفرست."
        )
        return

    if step == "description":
        context.user_data["description"] = (
            None if message.text == "-" else message.text
        )

        resource_type = context.user_data["resource_type"]

        if resource_type == "link":
            context.user_data["add_step"] = "payload"
            await message.reply_text("🔗 لینک منبع رو بفرست:")
        else:
            context.user_data["add_step"] = "payload"

            prompts = {
                "pdf": "📄 فایل PDF رو ارسال کن:",
                "questions": "📝 فایل نمونه سوال رو ارسال کن:",
                "video": "🎥 ویدیوی منبع رو ارسال کن:",
                "voice": "🎙 وویس منبع رو ارسال کن:",
                "audio": "🔊 فایل صوتی رو ارسال کن:"
            }

            await message.reply_text(prompts[resource_type])
        return

    if step == "payload":
        resource_type = context.user_data["resource_type"]
        file_id = None
        link = None

        if resource_type == "link":
            if not message.text:
                await message.reply_text("لطفاً لینک رو به صورت متن بفرست.")
                return
            link = message.text

        elif resource_type in ["pdf", "questions"]:
            if not message.document:
                await message.reply_text("لطفاً فایل رو به صورت Document ارسال کن.")
                return
            file_id = message.document.file_id

        elif resource_type == "video":
            if not message.video:
                await message.reply_text("لطفاً ویدیو رو با گزینه ارسال ویدیو بفرست.")
                return
            file_id = message.video.file_id

        elif resource_type == "voice":
            if not message.voice:
                await message.reply_text("لطفاً یک پیام وویس ارسال کن.")
                return
            file_id = message.voice.file_id

        elif resource_type == "audio":
            if not message.audio:
                await message.reply_text("لطفاً فایل صوتی ارسال کن.")
                return
            file_id = message.audio.file_id

        add_resource(
            title=context.user_data["title"],
            category=context.user_data["category"],
            resource_type=resource_type,
            file_id=file_id,
            link=link,
            description=context.user_data["description"]
        )

        context.user_data.clear()

        await message.reply_text(
            "✅ منبع با موفقیت ذخیره شد."
        )



# ==================================================
# Main
# ==================================================

def main():

    # ساخت جدول‌ها

    create_tables()


    # ساخت Application

    app = ApplicationBuilder().token(
        BOT_TOKEN
    ).build()


    # /start

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # دکمه‌ها

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )


    # دریافت فایل

    app.add_handler(
    MessageHandler(
        filters.TEXT
        | filters.Document.ALL
        | filters.VIDEO
        | filters.VOICE
        | filters.AUDIO,
        admin_add_message
    )
)

    app.add_handler(

        CommandHandler(
            "myid", my_id

        )
    )

    app.add_handler(
        CommandHandler(
        "admin", admin_panel

        )
    )

    logger.info(
        "Bot is starting..."
    )


    # اجرای ربات

    app.run_polling()


# ==================================================
# اجرای برنامه
# ==================================================

if __name__ == "__main__":

    main()

