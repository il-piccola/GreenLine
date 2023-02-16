import os
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
        'mode_admin' : False,
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
    employee = get_employee(request, False)
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
        ext = os.path.splitext(path)[1][1:]
        content_type = 'application/pdf'
        if ext == "xlsx" :
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif ext == "xls" :
            content_type = 'application/vnd.ms-excel'
        with open(file=path, mode='rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = 'inline;filename="'+ f.name + '"'
            return response
    except FileNotFoundError :
        return HttpResponse("ファイルが見つかりません")

@csrf_exempt
def admin_login(request) :
    params = {
        'title' : 'Administor Login',
        'msg' : '',
        'form' : LoginForm(),
        'mode_admin' : True,
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
            if data.first().auth :
                request.session['employee'] = data.first().id
                return redirect('admin_main')
            else :
                params['msg'] = '管理者権限がありません'
    else :
        params['msg'] = '入力に誤りがあります'
    params['form'] = form
    return render(request, 'login.html', params)

@csrf_exempt
def admin_main(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Administrator Main',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
    }
    return render(request, 'admin_main.html', params)

@csrf_exempt
def show_employees_list(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Employees List',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'list' : Employee.objects.all(),
    }
    return render(request, 'show_employees_list.html', params)

@csrf_exempt
def add_pdf(request) :
    pass

@csrf_exempt
def show_pdf_list(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'PDF List',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'list' : Pdf.objects.all(),
    }
    return render(request, 'show_pdf_list.html', params)

def get_employee(request, auth_flg) :
    if not 'employee' in request.session :
        return None
    employee = Employee.objects.filter(id=request.session['employee']).first()
    if not employee :
        return None
    if auth_flg and not employee.auth :
        return None
    return employee
