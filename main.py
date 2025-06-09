from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from keep_alive import keep_alive
import pandas as pd
import os
import re

# Load the CSV
df = pd.read_csv("MobilePrefixes.csv")

# Preprocess number ranges to regex
def convert_range_to_regex(number_range):
    regex = number_range.replace('x', r'\d').replace('-', '')
    return re.compile(f"^{regex}$")

# Precompile all regexes for performance
compiled_ranges = [(convert_range_to_regex(row["Number Range"]), row["Operators"]) for _, row in df.iterrows()]

# Handler for messages
async def lookup(update, context):
    user_input = update.message.text.strip()
    phone_number = re.sub(r'\D', '', user_input)  # Keep only digits

    for pattern, operator in compiled_ranges:
        if pattern.match(phone_number):
            await update.message.reply_text(f"📞 Operator: {operator}")
            return

    await update.message.reply_text("❌ Number not found in database.")

# Start command
async def start(update, context):
    await update.message.reply_text("Send me a Mauritian phone number (e.g., 52531234) and I’ll find the operator.")

# Start the bot
keep_alive()
app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lookup))
app.run_polling()
