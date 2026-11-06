from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.shortcuts import render, redirect

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'index-login.html')
    
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is None:
        messages.error(request, 'Usuário ou senha inválidos. ')
        return redirect('auth-login')
    
    login(request, user)
    return redirect('nucleo-inicial')

    # Parte que em teoria substituiria a parte acima:
    # user = authenticate(request,...).....return redirect('auth-login)
    # print('User', user)
    # if user is not None:
    #     login(request, user)
    #     return redirect('nucleo-inicial')
    # else:
    #     return redirect('auth-login')

def logout_view(request):
    logout(request)
    return redirect('auth-login')
