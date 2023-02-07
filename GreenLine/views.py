from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import *

def login(request) :
    params = {
        'title' : 'Login',
        'msg' : '',
        'form' : LoginForm(),
    }
    if 'msg' in request.session :
        params['msg'] = request.session['msg']
        request.session.clear()
    if (request.method != 'POST') :
        return render(request, 'login.html', params)
    obj = Member()
    form = LoginForm(data=request.POST, instance=obj)
    if form.is_valid() :
        data = Member.objects.filter(mail=request.POST['mail'])
        if data.count() <= 0 :
            params['msg'] = '未登録のメールアドレスです'
        else :
            item = data.first()
            if item.approval == False :
                params['msg'] = 'こちらからの電話確認後にユーザ認証されるまでお待ちください'
            else :
                return redirect('http://www.yahoo.co.jp')
    else :
        params['msg'] = '入力に誤りがあります'
    params['form'] = form
    return render(request, 'login.html', params)
