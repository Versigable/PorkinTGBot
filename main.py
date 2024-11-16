from telegram import InlineQueryResultPhoto, InputTextMessageContent, Bot
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
from io import BytesIO
from PIL import Image
import os
import logging
import base64
import uuid

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('PORKIN_BOT_TOKEN')

# Assuming your character image is in 'character.png' file
CHARACTER_PATH = 'character.png'

# Function to overlay the character
def overlay_image(base64_image):
    # Load the character image
    character = Image.open(CHARACTER_PATH)
    # Decode the base64 image to a PIL Image object
    base_image = Image.open(BytesIO(base64.b64decode(base64_image.split(',')[1])))
    # Perform overlay logic here
    # For simplicity, let's just paste the character in the top-left corner
    base_image.paste(character, (0,0), character)
    # Convert back to base64
    buffered = BytesIO()
    base_image.save(buffered, format="PNG")
    return buffered.getvalue()

def inlinequery(update, context):
    query = update.inline_query.query
    if not query:
        return

    # Process the image from the user's query
    try:
        processed_image_data = overlay_image(query)
        
        results = [
            InlineQueryResultPhoto(
                id=str(uuid.uuid4()),
                photo_url="data:image/png;base64," + base64.b64encode(processed_image_data).decode('utf-8'),
                thumb_url="data:image/png;base64," + base64.b64encode(processed_image_data)[:400].decode('utf-8')  # Thumbnail
            )
        ]
        update.inline_query.answer(results)
    except Exception as e:
        logger.error(f"Error in inline query handler: {e}")

def main():
    # Clear any existing webhook
    bot = Bot(token=TOKEN)
    webhook_info = bot.get_webhook_info()
    if webhook_info.url:
        logger.info("Clearing existing webhook")
        bot.delete_webhook()
    else:
        logger.info("No webhook to clear")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Start the bot
    logger.info("Starting bot polling")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
