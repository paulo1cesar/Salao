from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate


def home(request):
    return render(request, 'index.html')

def login(request):
    data = {}

    # Use get para acessar os valores, evitando MultiValueDictKeyError
    password = request.POST.get('password')
    re_password = request.POST.get('re-password')

    if password is not None and re_password is not None:
        if password != re_password:
            data['msg'] = 'As senhas estão diferentes!'
            data['class'] = 'alert-danger'
        else:
            # Crie o usuário e salve no banco de dados
            user = User.objects.create_user(request.POST.get('name'), request.POST.get('email'), password)
            user.save()

            # Defina uma mensagem de sucesso se as senhas estiverem iguais
            data['msg'] = 'Registro bem-sucedido!'
            data['class'] = 'alert-success'
    else:
        data['msg'] = 'Campos de senha não encontrados na requisição.'
        data['class'] = 'alert-danger'

    return render(request, 'login.html', data)

def user_login(request):
    data = {}
    userEmail = request.POST.get('email')
    userPassword = request.POST.get('password')

    # ... (seu código para verificar senhas)

    if userPassword is not None and userEmail is not None:

        # Autentique o usuário
        authenticated_user = authenticate(username=request.POST.get('name'), password=userPassword)

        if authenticated_user:
                # Faça login do usuário
            login(request, authenticated_user)

            # Redirecione para a página inicial
            return redirect('home')
        else:
            data['msg'] = 'Falha ao autenticar o usuário.'
            data['class'] = 'alert-danger'
    else:
        data['msg'] = 'Campos de senha não encontrados na requisição.'
        data['class'] = 'alert-danger'

    return render(request, 'login.html', data)

def csrf_failure_view(request, reason=""):
    return render(request, 'csrf_failure.html', {'reason': reason})
