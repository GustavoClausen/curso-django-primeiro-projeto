from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Insira o seu nome')
        add_placeholder(self.fields['last_name'], 'Insira o seu sobrenome')
        add_placeholder(self.fields['username'],
                        'Exemplo: João_Silva')
        add_placeholder(self.fields['email'], 'Exemplo: seunome@email.com')

    first_name = forms.CharField(
        error_messages={'required': 'Este campo é obrigatório.'},
        # required=True,    Já é true por padrão
        label='Nome',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Este campo é obrigatório.'},
        # required=True,    Já é true por padrão
        label='Sobrenome',
    )

    username = forms.CharField(
        label='Usuário',
        min_length=4,
        max_length=150,
        help_text='De 4 a 150 caracteres. Letras, números ou @/./+/-/_ apenas.',  # noqa 501
        error_messages={
            'min_length': 'Usuário deve possuir no mínimo 4 caracteres.',
            'max_length': 'Usuário deve possuir no máximo 150 caracteres.',
        }
    )

    email = forms.EmailField(
        # required=True,    Já é true por padrão
        error_messages={'required': 'Este campo é obrigatório.'},
        label='E-mail',
    )

    password = forms.CharField(
        # required=True,    Já é true por padrão
        label=('Senha'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Insira uma senha',
        }),
        help_text='A senha deve ter no mínimo 10 caracteres.',
        validators=[strong_password],
    )

    password2 = forms.CharField(
        # required=True,    Já é true por padrão
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
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exist = User.objects.filter(email=email).exists()

        if exist:
            raise ValidationError(
                'O e-mail informado já está em uso',
                code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            erro = ValidationError(
                'As senhas inseridas são diferentes.',
                code='invalid',
            )
            raise ValidationError({
                'password': erro,
            })
