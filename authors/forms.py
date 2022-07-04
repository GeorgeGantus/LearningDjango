import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_value):
    current_value = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{current_value} {attr_new_value}'.strip()


def add_placeholder(field, placeholder):
    add_attr(field, 'placeholder', placeholder)


def check_last_name(last_name):
    if last_name == 'Gantus':
        raise ValidationError(
            ('Last name could not be Gantus'), code='invalid')


class RegisterForm(forms.ModelForm):
    # 1 - first way of changing field attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['password'], 'Type your password here')

    # 2 - second way of changing field attributes
    # create or overwrite a field
    # overwrite if use the field name as variavle Ex.: password
    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        label="Password verification"
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Doe'
        }),
        validators=[check_last_name],
        label='Last name'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        # is possible to add other specials vars here like label that set the
        # label text for each var

        help_texts = {
            'email': 'The e-mail must be valid.',
            'password': 'The password must have at least one uppercase letter,'
            'one lowercase letter and one number. The length should be at'
            'least 8 characters'
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty'
            }
        }
        # 3 - third way of changind field attrs
        # changing the field
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your username here'
            }),
        }

        # to validate each field you need to write a method named
        # clean_field_name
    def clean_password(self):
        data = self.cleaned_data["password"]
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
        if not regex.match(data):
            raise ValidationError((
                'Password must have at least one uppercase letter, '
                'one lowercase letter and one number. The length '
                'should be at least 8 characters.'
            ),
                code='invalid'
            )
        return data

        # validate fields together
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            password_confirmation_error = ValidationError(
                'Password and Password verification must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password_confirm': [
                    password_confirmation_error,
                ],
            })
