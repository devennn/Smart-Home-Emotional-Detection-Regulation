import telegram

with open('smartzh.txt', 'r') as f:
    TOKEN = f.read().strip()

def send_telegram_mesg(msg, chat_id, token=TOKEN):
    print("To Telegram data: {}".format(msg))
    bot = telegram.Bot(token=token)
    try:
        bot.sendMessage(chat_id=chat_id, text=msg)
    except telegram.error.BadRequest:
        print("Send to Telegram error. Is your chat_id correct?")
