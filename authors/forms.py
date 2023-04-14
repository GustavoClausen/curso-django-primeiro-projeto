from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_value):
    field.widget.attrs['placeholder'] = f'{placeholder_value}'.strip()


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Insira seu nome')
        add_placeholder(self.fields['last_name'], 'Insira seu sobrenome')
        add_placeholder(self.fields['username'],
                        'Insira o nome do seu usuário')
        add_placeholder(self.fields['email'], 'Insira seu e-mail')
        add_placeholder(self.fields['password'], 'Insira uma senha')

    password2 = forms.CharField(
        required=True,
        label=('Confirme a senha'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita a senha inserida',
        }),
        # error_messages={
        #     'required': 'A senha é obrigatória.'
        # },
        help_text=('A senha deve ter pelo menos 10 caracteres.'),
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
                'placeholder': 'Insira o seu nome aqui',
                'class': 'input text-input teste',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Insira o seu sobrenome aqui'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'exemplo@email.com.br'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Insira a sua senha aqui'
            })
        }
