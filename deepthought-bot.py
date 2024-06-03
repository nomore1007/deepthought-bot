import subprocess
import os
from telegram.ext import Updater, CommandHandler, MessageHandler

# Set the API token for your bot
API_TOKEN = "YOUR-API-TOKEN"

def start(update, context):
    """Start command handler"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a Fabric/oLLaMa bot")

def help(update, context):
    """Help command handler"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="/start - Start the conversation\n/help - Show this message\n/list - lists the Fabric patterns\n/fabric - /fabric summarize [link]/or reply to")

def list(update, context):
    """List patterns handler"""
    result = subprocess.run(["fabric", "--list"], stdout=subprocess.PIPE)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result.stdout.decode('utf-8'))

def fabric(update, context):
    """Fabric command handler"""
    text = update.message.text
    reply = update.message.reply_to_message
    if text:
      args = text.split(" ",2)
    command = args[1]
    prompt = ""

    if reply:
      link = reply.text
    elif args[2]:
      link = args[2]
    else:
      context.bot.send_message(chat_id=update.effective_chat.id, text=result.stdout.decode('utf-8'))

    link = "https"+link.split("https",1)[1]
    link = link.split(" ",1)[0]

    if link and "www.youtube.com" in link:
      prompt = "yt --transcript \""
    else:
      prompt = " echo \""

    prompt = prompt + link + "\" | fabric --pattern " + command
    result = subprocess.run([prompt], shell=True, stdout=subprocess.PIPE)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result.stdout.decode('utf-8'))

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Adding handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", list))
    dp.add_handler(CommandHandler("fabric", fabric))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
