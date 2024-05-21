import requests
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm


def login_view(request):
    if request.method == 'POST':
        print("Se está intentando el envío del formulario...")
        register_form = RegisterForm(request.POST)
        login_form = LoginForm(request.POST)
        if 'login' in request.POST and login_form.is_valid():
            print("Intentado el login...")
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            response = requests.post('http://localhost:9000/api/login/',
                                     data={'username': username, 'password': password})
            if response.status_code == 200:
                request.session['token'] = response.json()['token']
                return redirect('home')
            else:
                return render(request, 'login.html', {
                    'login_form': login_form,
                    'register_form': register_form,
                    'login_error': 'Login Error',
                })
        elif 'register' in request.POST and register_form.is_valid():
            print("Intentando el registro...")
            email = register_form.cleaned_data['email']
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']

            response = requests.post('http://localhost:9000/api/register/',
                                     data={'email': email, 'username': username, 'password': password})
            if response.status_code == 201:
                print("Se ha registrado correctamente")
                request.session['token'] = response.json()['token']
                return redirect('home')
            else:
                return render(request, 'login.html', {
                    'login_form': login_form,
                    'register_form': register_form,
                    'register_error': 'Error during register',
                })
    else:
        register_form = RegisterForm(request.POST)
        login_form = LoginForm(request.POST)
    return render(request, 'login.html', {
        'login_form': login_form, 'register_form': register_form
    })


def logout_view(request):
    request.session.flush()
    return redirect('login')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        token = request.session.get('token')
        print(token)
        if not token:
            return redirect('login')

        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:9000/api/user/', headers=headers)
        print(response)
        if response.status_code != 200:
            return redirect('login')

        user_data = response.json()
        return self.render_to_response(self.get_context_data(user=user_data))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = kwargs.get('user')
        return context
