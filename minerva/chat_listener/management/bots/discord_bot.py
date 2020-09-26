import logging

import discord

from minerva.chat_listener.management.bots.utils import log_message, running_bot_with_token_log
from minerva.core.models import ChatApp, store_message, add_user
from minerva.core.signals import message_stored


class DiscordBot(discord.Client):
    def __init__(self, token, **options):
        super().__init__(**options)
        self.token = token
        self.chat_app, _ = ChatApp.objects.get_or_create(name='Discord')

        logging.info('Starting up Discord bot')

    def run_bot(self):
        self.run(self.token)
        running_bot_with_token_log(self, type(self).__name__)

    async def on_message(self, message: discord.Message):
        logging.info('Message received on Discord bot: %s' % message.content)
        sender_id = message.author.id
        sender_name = message.author.name

        log_message(message.content, sender_id, sender_name, self.chat_app.name)

        chat_group_name = '{}.{}'.format(message.guild.name, message.channel.name)

        new_message = store_message(
            chat_app=self.chat_app,
            chat_group_id=message.channel.id,
            chat_group_name=chat_group_name,
            message_id=message.id,
            message_content=message.content,
            sender_id=sender_id,
            sender_name=sender_name,
            message_date=message.created_at,
            sender_obj=message.author,
            new_user_callback=self.send_welcome_message,
            edit_date=message.edited_at,
            sender_email=message.author.email)

        message_stored.send(self.__class__, message=new_message)

    async def on_member_join(self, member):
        for channel in member.guild.channels:
            add_user(
                chat_app=self.chat_app,
                chat_group_id=channel.id,
                user_app_id=member.id,
                user_name=member.name
            )
            logging.info('Member %s joined channel %s' % (member.id, channel.id))

    async def on_guild_join(self, guild: discord.Guild):
        pass

    async def send_welcome_message(self, user):
        pass
