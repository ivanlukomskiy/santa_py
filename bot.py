from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

token = None
with open("TELEGRAM_TOKEN_FILE", 'r') as file:
    token = file.read().replace('\n', '')


receiver_by_sender = {}

with open("dist.txt", 'r') as file:
    for line in file.readlines():
        line = line.strip()
        if line:
            sender, receiver = line.split(',')
            receiver_by_sender[sender.lower()] = receiver.lower()


def start(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    username = update.message.from_user['username']
    print(f'Got message from {username}: {text}')
    if username in receiver_by_sender:
        recipient = receiver_by_sender[username]
        response = f"Ты даришь @{recipient}"
    else:
        response = "Я тебя не знаю"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    start_handler = MessageHandler(Filters.text, start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
