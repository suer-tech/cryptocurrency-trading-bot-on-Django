from django.apps import AppConfig

from core.services.base import create_profitA_list, create_profitB_list, create_equity_list, create_lossA_list, \
    create_lossB_list
from core.services.txt import create_txt
from core.trading import start_trade
from core.views.telegrammer import message_sender_thread


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        create_profitA_list()
        create_profitB_list()
        create_equity_list()
        create_lossA_list()
        create_lossB_list()
        create_txt()
        start_trade.start()

        if not message_sender_thread.is_alive():
            message_sender_thread.start()
