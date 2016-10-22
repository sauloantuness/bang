from django.forms import ModelForm, TextInput, SelectMultiple, ValidationError
from home.models import Team

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'profiles']
        widgets = {
            'name': TextInput(
            	attrs={
            		'autocomplete': 'off',
            		'placeholder': 'My Team',
            		'required': 'required',
            		'autofocus': 'true',
            		'class': 'form-control'
            	}
            ),
            'profiles': SelectMultiple(
            	attrs={
            		'class': 'form-control selectpicker',
            		'data-live-search': 'true',
					'name': 'profiles',
					'title': 'select',
					'data-max-options': 3
            	}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TeamForm, self).__init__(*args, **kwargs)

    def clean_profiles(self):
        profiles = self.cleaned_data['profiles']
        if self.request.user.profile not in profiles:
            raise ValidationError("You need to be on the team")
        return profiles

