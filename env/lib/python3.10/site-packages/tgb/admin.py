from django.contrib import admin

from .models import Profile, Message
from .forms import ProfileForm, MessageForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_name', 'user_id')
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_text', 'when_message')
    form = MessageForm


