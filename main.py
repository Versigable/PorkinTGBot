from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
from io import BytesIO
import os

TOKEN = os.getenv('PORKIN_BOT_TOKEN')
STOCK_IMAGE_PATH = '/root/PorkinTGBot/porkin_images/porkin1.jpg'  # Ensure this path is correct
last_photo = {}

def overlay_image(user_image, stock_image_path):
    """Overlay user image with stock image."""
    user_img = Image.open(user_image)
    stock_img = Image.open(stock_image_path)
    
    # Resize stock image if needed to fit on top of the user image
    stock_img = stock_img.resize(user_img.size)
    
    # Overlay logic (simple paste here)
    user_img.paste(stock_img, (0,0), stock_img)
    
    # Save the result to a BytesIO object for sending
    result = BytesIO()
    user_img.save(result, format="PNG")
    result.seek(0)
    return result

def handle_photo(update, context):
    """Store the last photo sent in the chat."""
    chat_id = update.message.chat_id
    last_photo[chat_id] = update.message.photo[-1].file_id

def porkin_command(update, context):
    """Handle the /porkin command to overlay images."""
    chat_id = update.message.chat_id
    
    if chat_id in last_photo:
        file_id = last_photo[chat_id]
        new_file = context.bot.get_file(file_id)
        with BytesIO() as user_image:
            new_file.download(out=user_image)
            user_image.seek(0)
            
            # Process image
            processed_image = overlay_image(user_image, STOCK_IMAGE_PATH)
            
            # Send the processed image back
            context.bot.send_photo(chat_id=chat_id, photo=processed_image)
    else:
        update.message.reply_text("Please upload an image before using /porkin.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Handler for photos
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    
    # Handler for the /porkin command
    dp.add_handler(CommandHandler("porkin", porkin_command))
    
    updater.start_polling(poll_interval=1.0, timeout=30)
    updater.idle()

if __name__ == '__main__':
    main()
