from django.shortcuts import render
from django.shortcuts import redirect
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

@csrf_exempt
def login(request) :
    params = {
        'title' : 'Login',
        'msg' : '',
        'form' : LoginForm(),
    }
    if 'msg' in request.session :
        params['msg'] = request.session['msg']
        del request.session['msg']
    if (request.method != 'POST') :
        return render(request, 'login.html', params)
    obj = Employee()
    form = LoginForm(data=request.POST, instance=obj)
    if form.is_valid() :
        data = Employee.objects.filter(mail=request.POST['mail'])
        if data.count() <= 0 :
            params['msg'] = '未登録のメールアドレスです'
        else :
            request.session['employee'] = data.first().id
            return redirect('main')
    else :
        params['msg'] = '入力に誤りがあります'
    params['form'] = form
    return render(request, 'login.html', params)

@csrf_exempt
def main(request) :
    if not 'employee' in request.session :
        return redirect('login')
    employee = Employee.objects.filter(id=request.session['employee']).first()
    if not employee :
        return redirect('login')
    params = {
        'title' : 'Main',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'form' : MainForm(),
    }
    if (request.method != 'POST') :
        return render(request, 'main.html', params)
    else :
        form = MainForm(data=request.POST)
        if form.is_valid() :
            pdf = Pdf.objects.filter(phone=form.cleaned_data['phone'])
            if pdf and pdf.count() > 0 :
                params['pdf'] = pdf
            else :
                params['msg'] = '該当するPDFファイルがありません'
            params['form'] = form
        else :
            params['msg'] = '入力に誤りがあります'
    return render(request, 'main.html', params)

@csrf_exempt
def show_pdf(request) :
    phone = request.POST.get('phone')
    pdf = Pdf.objects.filter(phone=phone)
    if not pdf or pdf.count() <= 0 :
        return HttpResponse("ファイルが見つかりません")
    try :
        path = pdf.first().get_path()
        with open(file=path, mode='rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename="'+ f.name + '"'
            return response
    except FileNotFoundError :
        return HttpResponse("ファイルが見つかりません")

