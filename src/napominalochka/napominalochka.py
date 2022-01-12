import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def pulse(context: CallbackContext) -> None:
    context.bot.send_message(context.job.context, text='tap')


def start(update: Update, context: CallbackContext) -> None:
    if (str(update.message.chat_id) == TELEGRAM_CHAT_ID
            and str(update.message.from_user.id) == TELEGRAM_USER_ID):
        context.job_queue.run_repeating(
            pulse,
            3,
            None,
            None,
            context=update.message.chat_id
        )
        update.message.reply_text('pulse started')
    else:
        update.message.reply_text('access denied')


def stop(update: Update, context: CallbackContext) -> bool:
    if (str(update.message.chat_id) == TELEGRAM_CHAT_ID
            and str(update.message.from_user.id) == TELEGRAM_USER_ID):
        current_jobs = context.job_queue.get_jobs_by_name('pulse')
        if not current_jobs:
            update.message.reply_text('pulse wasn\'t found')
        for job in current_jobs:
            job.schedule_removal()
        update.message.reply_text('pulse stopped')
    else:
        update.message.reply_text('access denied')


def main() -> None:
    updater = Updater(TELEGRAM_API_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stop', stop))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
