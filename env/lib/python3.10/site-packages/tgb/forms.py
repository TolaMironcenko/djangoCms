from dataclasses import fields
from django import forms

from .models import Profile, Message

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'name',
            'user_name',
            'user_id',
        )
        widgets = {
            'name': forms.TextInput,
            'user_name': forms.TextInput,
            'user_id': forms.TextInput
        }

    
class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = (
            'message_text',
            'when_message',
            'for_all',
        )
