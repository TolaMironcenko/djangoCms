from tabnanny import verbose
from django.db import models
import datetime


class Profile(models.Model):
    name = models.TextField(
        verbose_name="имя аккаунта"
    )
    user_name = models.TextField(
        verbose_name="имя пользователя"
    )
    user_id = models.PositiveIntegerField(
        verbose_name="chatid gользователя",
        unique=True
    )

    class Meta:
        verbose_name="tg профиль"
        verbose_name_plural="tg профили"

    def __str__(self):
        return f'{self.name} {self.user_name}'


class Message(models.Model):
    message_text = models.TextField(
        verbose_name="текст сообщения"
    )
    when_message = models.DateTimeField(
        verbose_name="когда отправить"
    )
    for_all = models.BooleanField(
        verbose_name='для всех пользователей',
        default=False
    )

    def __str__(self):
        return f'{self.message_text} {self.when_message.strftime("%Y-%m-%d %H:%M" + ":00")}'