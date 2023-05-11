from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

from .forms import LoginForm, RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'author/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
        'not_show_search_input': True,
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        userData = form.save(commit=False)
        userData.set_password(userData.password)
        userData.save()
        messages.success(request, 'Usuário criado com sucesso.')

        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'author/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
        'not_show_search_input': True,
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Login realizado com sucesso.')
            login(request, authenticated_user)

        else:
            messages.error(request, 'Usuário ou senha inválido.')

    else:
        messages.error(request, 'Erro na validação do formulário.')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Requisicao de logout invalida.')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Requisicao de logout negada.')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Deslogado com sucesso.')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request,
        'author/pages/dashboard.html',
        context={
            'recipes': recipes,
            'not_show_search_input': True,
        }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    # Podemos usar get() também

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        request.POST or None,
        instance=recipe
    )

    return render(
        request,
        'author/pages/dashboard_recipe.html',
        context={
            'form': form,
            'not_show_search_input': True,
        }
    )
