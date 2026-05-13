import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = os.environ.get("TOKEN")
GAME_URL = "https://zooma-57c.pages.dev"
STATS_URL = "https://zooma-stats.selcanburakgazi6697.workers.dev"
STATS_KEY = "zooma2026stats"
ADMIN_IDS = [8101681923]

bot = telebot.TeleBot(TOKEN)

ANIMATION_FILE_ID = None

def ping(event, uid="anon"):
    try:
        requests.get(f"{STATS_URL}/ping", params={"event": event, "uid": uid}, timeout=3)
    except:
        pass

def get_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "🦈 Играть в Zooma Lucky Spin",
        web_app=WebAppInfo(url=GAME_URL)
    ))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global ANIMATION_FILE_ID
    uid = str(message.from_user.id)
    ping("start", uid)

    caption = "🦈 Добро пожаловать в Zooma Lucky Spin!\n\nНажми кнопку и испытай удачу 👇"
    markup = get_markup()

    if ANIMATION_FILE_ID:
        bot.send_animation(message.chat.id, ANIMATION_FILE_ID, caption=caption, reply_markup=markup)
    else:
        video_path = os.path.join(os.path.dirname(__file__), "zooma.mp4")
        if os.path.exists(video_path):
            with open(video_path, "rb") as f:
                sent = bot.send_animation(message.chat.id, f, caption=caption, reply_markup=markup)
                ANIMATION_FILE_ID = sent.animation.file_id
        else:
            bot.send_message(message.chat.id, caption, reply_markup=markup)

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        r = requests.get(f"{STATS_URL}/stats", params={"key": STATS_KEY}, timeout=5)
        d = r.json()
        text = (
            f"📊 Zooma Lucky Spin — Статистика\n\n"
            f"Всего:\n"
            f"  🚀 /start: {d['total']['starts']}\n"
            f"  👁 Визитов: {d['total']['visits']}\n"
            f"  🎰 Спинов: {d['total']['spins']}\n"
            f"  🔗 Кликов: {d['total']['clicks']}\n\n"
            f"Уникальных:\n"
            f"  🚀 /start: {d['unique']['starts']}\n"
            f"  👤 Посетителей: {d['unique']['visits']}\n"
            f"  🔗 Перешли: {d['unique']['clicks']}\n\n"
            f"Сегодня:\n"
            f"  🚀 /start: {d['today']['starts']}\n"
            f"  👁 Визитов: {d['today']['visits']}\n"
            f"  🎰 Спинов: {d['today']['spins']}\n"
            f"  🔗 Кликов: {d['today']['clicks']}\n\n"
            f"📈 CTR: {d['ctr']}"
        )
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

print("Bot started...")
bot.infinity_polling()
