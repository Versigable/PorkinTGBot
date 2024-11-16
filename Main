from telegram import InlineQueryResultPhoto, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
from io import BytesIO
from PIL import Image

TOKEN = 'YOUR_API_TOKEN_HERE'

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
    if query == '':
        return

    # Here you would process the image from the user's query
    # For simplicity, we'll simulate image processing here:
    processed_image_data = overlay_image(query)  # This should be updated to process actual image data
    
    results = [
        InlineQueryResultPhoto(
            id=str(uuid.uuid4()),
            photo_url="data:image/png;base64," + base64.b64encode(processed_image_data).decode('utf-8'),
            thumb_url="data:image/png;base64," + base64.b64decode(processed_image_data)[:400].decode('utf-8')  # Thumbnail
        )
    ]

    update.inline_query.answer(results)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
