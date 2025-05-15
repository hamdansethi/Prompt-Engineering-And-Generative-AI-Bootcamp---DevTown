# import os
# import re
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# load_dotenv()

# os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# groq_api_key = os.getenv("GROQ_API_KEY")

# def setup_llm_chain(topic="technology"):
#     prompt = ChatPromptTemplate(
#         [
#             ("system", "You are a Standup Comedian, just give me a joke on the given topic."),
#             ("user", "topic: {topic}")
#         ]
#     )

#     model = ChatGroq(
#         model = "Gemma2-9b-It", 
#         groq_api_key=groq_api_key
#         )
    

#     return prompt|model|StrOutputParser()

# async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Hi, mention me with a topic like '@jjoke_bbot python' to get a joke")

# async def help(update:Update, context:ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Mention me with a topic like '@jjoke_bbot python' to get a joke")

# async def generate_joke(update:Update, context:ContextTypes.DEFAULT_TYPE, topic: str):
#     await update.message.reply_text("Generating a joke about {topic}")
#     joke = setup_llm_chain(topic).invoke({}).strip()
#     await update.message.reply_text(joke)

# async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
#     msg = update.message.text
#     bot_username = context.bot.username

#     if f'@{bot_username}' in msg:
#         match = re.search(f'@{bot_username}\\s+(.*)', msg)
#         if match and match.group(1).strip():
#             await generate_joke(update, context, match.group(1).strip())
#         else:
#             await update.message.reply_text("Please specify a topic after mentioning me")

# def main():
#     token = os.getenv("TELEGRAM_API_KEY")
#     app = Application.builder().token(token).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("help", help))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#     app.run_polling(allowed_updates=Update.ALL_TYPES)

# if __name__ == "__main__":
#     main()

import os
import re
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------
# Setup Logging
# ----------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# ----------------------------
# LLM Chain Setup
# ----------------------------
def setup_llm_chain(topic="technology"):
    logger.info(f"Setting up LLM chain for topic: {topic}")

    prompt = ChatPromptTemplate(
        [
            ("system", "You are a Standup Comedian, just give me a joke on the given topic."),
            ("user", "topic: {topic}")
        ]
    )

    model = ChatGroq(
        model="Gemma2-9b-It",
        groq_api_key=groq_api_key
    )

    return prompt | model | StrOutputParser()

# ----------------------------
# Bot Commands
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/start command by {update.effective_user.username}")
    await update.message.reply_text("Hi, mention me with a topic like '@jjoke_bbot python' to get a joke")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/help command by {update.effective_user.username}")
    await update.message.reply_text("Mention me with a topic like '@jjoke_bbot python' to get a joke")

# ----------------------------
# Joke Generation
# ----------------------------
async def generate_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    logging.info(f"Generating joke for topic: {topic}")
    await update.message.reply_text(f"Generating a joke about {topic}")
    try:
        joke = setup_llm_chain(topic).invoke({"topic": topic}).strip()
        logging.info(f"Generated joke: {joke}")
        await update.message.reply_text(joke)
    except Exception as e:
        logging.error(f"Error generating joke: {e}")
        await update.message.reply_text("Sorry, I couldn't generate a joke right now.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    logging.debug(f"Received message: {msg}")
    bot_username = context.bot.username
    logging.debug(f"Bot username: {bot_username}")

    if f'@{bot_username}' in msg:
        match = re.search(f'@{bot_username}\\s+(.*)', msg)
        if match and match.group(1).strip():
            topic = match.group(1).strip()
            logging.info(f"Detected topic: {topic}")
            await generate_joke(update, context, topic)
        else:
            await update.message.reply_text("Please specify a topic after mentioning me")
# ----------------------------
# Main Entry Point
# ----------------------------
def main():
    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        raise ValueError("TELEGRAM_API_KEY not found in .env")

    logger.info("Starting Telegram bot...")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is now polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
