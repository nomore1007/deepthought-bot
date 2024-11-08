import os
import logging
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Set the API token for your bot
API_TOKEN = os.environ.get('api_token')
OLLAMA_SERVER = os.environ.get('ollama_server')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
       chat_id=update.effective_chat.id,
       text="Hi! I'm a Fabric-oLLaMa bot"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
       chat_id=update.effective_chat.id, 
       text="/start - Start the conversation\n/help - Show this message\n/list - lists the Fabric patterns\n/fabric - /fabric summarize [link]/or reply to"
    )

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = subprocess.run(["fabric --list --remoteOllamaServer "+OLLAMA_SERVER],
       shell=True, stdout=subprocess.PIPE
    )
    await context.bot.send_message(
       chat_id=update.effective_chat.id,
       text=result.stdout.decode('utf-8')
    )

async def fabric(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
      await context.bot.send_message(
         chat_id=update.effective_chat.id, text=result.stdout.decode('utf-8')
      )

    link = "https"+link.split("https",1)[1]
    link = link.split(" ",1)[0]

    if link and "www.youtube.com" in link:
      prompt = "yt --transcript \""
    else:
      prompt = " echo \""

    prompt = prompt + link + "\" | fabric --remoteOllamaServer " + OLLAMA_SERVER + " --pattern " + command + " --model ollam3:latest"
    result = subprocess.run([prompt], shell=True, stdout=subprocess.PIPE)
    await context.bot.send_message(
       chat_id=update.effective_chat.id, text=result.stdout.decode('utf-8')
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('list', list))
    application.add_handler(CommandHandler('fabric', fabric))

    application.run_polling()
