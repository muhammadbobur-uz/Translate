from telegram import InlineKeyboardButton
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, InlineQueryHandler, ConversationHandler, CallbackQueryHandler
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from lot_kir import translate

translit = translate()

STATE_TRANSLATE = 0
STATE_TWO = 1

button= [[InlineKeyboardButton("♻️ Кириллча", callback_data='1'), InlineKeyboardButton("♻️ Lotincha", callback_data='2')]]
global txt
txt = "❇️AgroZamin'da nimalarni topish mumkin?\n\nAgroZamin - turli toifadagi qishloq xo‘jaligi mahsulotlarini topish va xarid qilish mumkin bo‘lgan qulay onlayn-platforma." \
    "\n\nMahsulotlarni hoziroq joylashtirish mumkin bo‘lgan bo‘limlar:\n" \
    "-  Agrokimyo\n" \
    "-  Veterinariya\n" \
    "-  Agrotexnika va uskunalar uchun butlovchi qismlar\n" \
    "-  Gʻalla, urug‘ va ozuqalar\n" \
    "-  Bog‘ va tomorqa mahsulotlari\n" \
    "-  Qishloq xo‘jaligi texnikasi\n" \
    "-  Chorva hayvonlari va parrandalar\n" \
    "-  Maxsus kiyimlar va maxsus texnika\n" \
    "-  О‘g‘itlar\n" \
    "-  Va boshqa ko‘plab mahsulotlar\n"


def start(update:Update, context:CallbackContext):
    update.message.reply_html(f"🤖 Assalomu alaykum <b>{update.message.chat_id}</b>!\n\n♻️ Bot lotin matnni krilga o'girib beradi.\n✍🏻 Biror text kiriting...")
    context.bot.send_message(chat_id=update.message.chat_id, text="salom")
    update.message.reply_html(f"{update}")
    return STATE_TRANSLATE

def translat(update:Update, context:CallbackContext):
    text = update.message.text
    update.message.reply_html(f"{update}")
    if text == 'change':
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open("photo.jpg", "rb"), caption=txt, reply_markup=InlineKeyboardMarkup(button))
        return STATE_TWO

    try:
        try:
            context.bot.send_video(chat_id=update.message.chat_id, video=update.message['video']['file_id'],
                                   caption=translit.t_translit(update.message['caption']))
        except:
            context.bot.send_photo(update.message.chat_id, photo=update.message['photo'][0]['file_id'], caption=translit.t_translit(update.message['caption']))
    except:
        text = update.message.text
        t = translit.t_translit(text=text)
        update.message.reply_html(f"{t}")


def change(update:Update, context:CallbackContext):
    query = update.callback_query
    if query.data == '1':
        print(query.data)
        query.edit_message_caption(caption=translit.t_translit(txt), reply_markup=InlineKeyboardMarkup(button))
    if query.data == '2':
        query.edit_message_caption(caption=txt, reply_markup=InlineKeyboardMarkup(button))


updater = Updater('Token', use_context=True)


conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.all, start)
    ],
    states = {
        STATE_TRANSLATE: [
            MessageHandler(Filters.all, translat)
        ],
        STATE_TWO: [
            CallbackQueryHandler(change)
        ]
    },
    fallbacks= [MessageHandler(Filters.all, start)]
)
updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()

