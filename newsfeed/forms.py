from django import forms
from newsfeed.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from djangotoolbox.fields import ListField


class RegistrationForm(UserCreationForm):
    gender_choice = (
        ('1', 'Male'),
        ('2', 'Female')
    )
    age_choice = (
        (1, '<18'),
        (2, '18-25'),
        (3, '26-45'),
        (4, '>45')
    )
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=gender_choice)
    age_group = forms.ChoiceField(choices=age_choice)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'age_group',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


# class idsForm(forms.Form):
#     ids = forms.ListField(forms.CharField(max_length=2000), default=[])