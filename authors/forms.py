import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            ('A senha precisa ter letras maísculas, minúsculas e números.'),
            code='Invalid'
        )

    return


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Insira o seu nome')
        add_placeholder(self.fields['last_name'], 'Insira o seu sobrenome')
        add_placeholder(self.fields['username'],
                        'Exemplo: João_Silva')
        add_placeholder(self.fields['email'], 'Exemplo: seunome@email.com')

    password = forms.CharField(
        required=True,
        label=('Senha'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Insira uma senha',
        }),
        help_text='A senha deve ter no mínimo 10 caracteres.',
        validators=[strong_password],
    )

    password2 = forms.CharField(
        required=True,
        label=('Confirme a senha'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita a senha inserida',
        }),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário',
            'email': 'E-mail',
            'password': 'Senha',
        }

        help_texts = {
            'email': '',
            'username': '',
        }

        # error_messages = {
        #     'username': {
        #         'required': 'Campo obrigatório',
        #     }
        # }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'testando-classe',
            }),
            'last_name': forms.TextInput(),
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Insira uma senha',
            })
        }

    def clean_password(self):

        data = self.cleaned_data.get('password')

        if 'teste' in data:
            raise ValidationError(
                'O valor %(value)s não é aceito',
                code='invalid',
                params={'value': '"teste"'},
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'Jose' in data:
            raise ValidationError(
                'O valor %(value)s não é aceito',
                code='invalid',
                params={'value': '"Jose"'},
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            erro = ValidationError(
                'As senhas inseridas são diferentes',
                code='invalid',
            )
            raise ValidationError({
                'password': erro,
            })
