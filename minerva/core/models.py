from django.db import models


class Message(models.Model):
    app_message_id = models.TextField(null=False)
    sent_date = models.DateTimeField(null=False)
    last_updated = models.DateTimeField(null=False)
    content = models.TextField(null=False, blank=False)
    normalized_content = models.TextField(null=True, blank=False)
    chat_group = models.ForeignKey('ChatGroup', null=False, on_delete=models.CASCADE)
    sent_by = models.ForeignKey('User', null=False, on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='replies')
    conversation = models.ForeignKey('Conversation', null=True, on_delete=models.DO_NOTHING)
    hashtags = models.ManyToManyField('Hashtag')


class Conversation(models.Model):
    first_message = models.ForeignKey('Message', null=False, on_delete=models.DO_NOTHING, related_name='+')
    hashtag = models.ForeignKey('Hashtag', null=False, on_delete=models.CASCADE)


class Hashtag(models.Model):
    content = models.TextField(null=False, blank=False, unique=True)


class User(models.Model):
    name = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=False)
    email = models.TextField(null=True, blank=False)


class ChatApp(models.Model):
    name = models.TextField(null=False, blank=False)
    bot_token = models.TextField(null=False, blank=False)

    #@property
    #def telegram(self):
    #    return self.objects.filter(name='Telegram').first()


class AppUsers(models.Model):
    user = models.ForeignKey('User', null=False, on_delete=models.CASCADE)
    app = models.ForeignKey('ChatApp', null=False, on_delete=models.CASCADE)
    user_app_id = models.TextField(null=False, blank=False)


class ChatGroup(models.Model):
    app_chat_id = models.TextField(null=False, blank=False)
    name = models.TextField(null=True, blank=True)
    application = models.ForeignKey('ChatApp', null=False, on_delete=models.CASCADE, related_name='chat_groups')
    members = models.ManyToManyField('User', related_name='chat_groups')
