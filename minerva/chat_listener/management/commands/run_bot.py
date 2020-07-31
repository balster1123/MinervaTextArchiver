from django.core.management.base import BaseCommand, CommandError
from minerva.chat_listener.management.bots.telegram_bot import TelegramBot

CHAT_BOTS = {
    'Telegram': (TelegramBot, '1091823005:AAGKv37qO50fTAQy79F-rmetz-KsHNvFStE')
}


class Command(BaseCommand):
    help = 'Run specified chat bot'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, nargs='?', default='Telegram')

    def handle(self, *args, **options):
        app = options['app']
        bot_type, token = CHAT_BOTS[app]
        bot_type(token).run()
