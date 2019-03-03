from django.forms import ModelForm

from .models import Settings


class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ['preferred_unit', 'preferred_colour']
