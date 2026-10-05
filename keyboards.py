
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


# -------------------------
# منوی اصلی
# -------------------------

def main_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🧠 آناتومی",
                callback_data="category_anatomy"
            ),

            InlineKeyboardButton(
                "🫀 فیزیولوژی",
                callback_data="category_physiology"
            )
        ],

        [
            InlineKeyboardButton(
                "🧪 بیوشیمی",
                callback_data="category_biochemistry"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 نمونه سوالات",
                callback_data="questions"
            )
        ],

        [
            InlineKeyboardButton(
                "🔍 جستجو",
                callback_data="search"
            )
        ],

        [
            InlineKeyboardButton(
                "⭐ ذخیره شده‌ها",
                callback_data="favorites"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# -------------------------
# دکمه بازگشت
# -------------------------

def back_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="home"
            )
        ]

    ]


    return InlineKeyboardMarkup(keyboard)

def admin_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "➕ افزودن منبع",
                callback_data="admin_add"
            )
        ],
        [
            InlineKeyboardButton(
                "📚 لیست منابع",
                callback_data="admin_list"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 حذف منبع",
                callback_data="admin_delete"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="home"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
def admin_category_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🧠 آناتومی", callback_data="addcat_anatomy"),
            InlineKeyboardButton("🫀 فیزیولوژی", callback_data="addcat_physiology")
        ],
        [
            InlineKeyboardButton("🧪 بیوشیمی", callback_data="addcat_biochemistry")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_type_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📄 PDF", callback_data="addtype_pdf"),
            InlineKeyboardButton("📝 نمونه سوال", callback_data="addtype_questions")
        ],
        [
            InlineKeyboardButton("🎥 ویدیو", callback_data="addtype_video"),
            InlineKeyboardButton("🎙 وویس", callback_data="addtype_voice")
        ],
        [
            InlineKeyboardButton("🔊 فایل صوتی", callback_data="addtype_audio"),
            InlineKeyboardButton("🔗 لینک", callback_data="addtype_link")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)