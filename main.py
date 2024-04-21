from bs4 import BeautifulSoup
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '6852701624:AAHLlPWsLL3qO70CmwAFE0RQELWQuYUhPbg'

async def scrape_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = ' '.join(context.args)
    if not url:
        await update.message.reply_text("Please provide a URL.")
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            target_div = soup.find('div', class_="col-md-6 col-lg-8 col-xl-6 offset-lg-6 d-none")
            if not target_div:
                await update.message.reply_text("Div not found.")
                return

            select_element = target_div.find('select', class_="form-control product-variant-input")
            if not select_element:
                await update.message.reply_text("Select element not found within the target div.")
                return

            options = select_element.find_all('option')
            response_text = ""
            for option in options:
                data_stock = option.get('data-stock')
                data_price = option.get('data-price')
                value_option = option.text
                response_text += f"{value_option.strip()} \nStock: {data_stock} \nPrice: {data_price}\n\n"

            await update.message.reply_text(response_text)
        else:
            await update.message.reply_text(f"Failed to fetch webpage, status code: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a URL to scrape.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Adding a start command and the scrape_site function to handle messages
    start_handler = CommandHandler('start', start)
    scrape_handler = CommandHandler('scrape', scrape_site)

    application.add_handler(start_handler)
    application.add_handler(scrape_handler)

    application.run_polling()

