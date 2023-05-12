import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
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
        data = Employee.objects.filter(phone=request.POST['phone'])
        if data.count() <= 0 :
            params['msg'] = '未登録のドライバー電話番号です'
        elif data.first().password != request.POST['password'] :
            params['msg'] = 'パスワードが間違っています'
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
        'shipper_list' : Shipper.objects.all(),
    }
    print(params['shipper_list'])
    if (request.method != 'POST') :
        return render(request, 'main.html', params)
    else :
        form = MainForm(data=request.POST)
        if form.is_valid() :
            consignees = Consignee.objects.filter(phone__contains=form.cleaned_data['phone'])
            files = File.objects.filter(consignee__in=consignees)
            if files and files.count() > 0 :
                params['files'] = files
            else :
                params['msg'] = '該当するPDFファイルがありません'
            params['form'] = form
        else :
            params['msg'] = '入力に誤りがあります'
    return render(request, 'main.html', params)

@csrf_exempt
def show_file(request) :
    phone = request.POST.get('phone')
    file = File.objects.filter(phone=phone)
    if not file or file.count() <= 0 :
        return HttpResponse("PDFファイルが見つかりません")
    try :
        path = File.first().get_path()
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
        return HttpResponse("PDFファイルが見つかりません")

@csrf_exempt
def change_password(request) :
    employee = get_employee(request, False)
    if not employee :
        return redirect('login')
    params = {
        'title' : 'Password',
        'msg' : 'パスワードを変更できます',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'form' : PasswordForm(),
    }
    if (request.method != 'POST') :
        return render(request, 'change_password.html', params)
    else :
        form = PasswordForm(data=request.POST)
        if form.is_valid() :
            new = request.POST['new']
            confirm = request.POST['confirm']
            if new == confirm :
                employee.password = new
                employee.save()
                request.session['msg'] = 'パスワードを変更しました、再度ログインしてください'
                del request.session['employee']
                return redirect('login')
            else :
                params['msg'] = '新パスワード(確認)が間違っています'
        else :
            params['msg'] = '入力に誤りがあります'
    return render(request, 'change_password.html', params)

@csrf_exempt
def admin_login(request) :
    params = {
        'title' : 'Admin Login',
        'msg' : '',
        'form' : LoginForm(),
        'mode_admin' : True,
    }
    if 'msg' in request.session :
        params['msg'] = request.session['msg']
        del request.session['msg']
    if request.method != 'POST' :
        return render(request, 'login.html', params)
    obj = Employee()
    form = LoginForm(data=request.POST, instance=obj)
    if form.is_valid() :
        data = Employee.objects.filter(phone=request.POST['phone'])
        if data.count() <= 0 :
            params['msg'] = '未登録の管理者電話番号です'
        elif data.first().password != request.POST['password'] :
            params['msg'] = 'パスワードが間違っています'
        elif not data.first().auth :
            params['msg'] = '管理者権限がありません'
        else :
            request.session['employee'] = data.first().id
            return redirect('admin_main')
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
        'title' : 'Admin Main',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
    }
    return render(request, 'admin_main.html', params)

@csrf_exempt
def show_employees(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Employees',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'list' : Employee.objects.all(),
    }
    return render(request, 'show_employees.html', params)

@csrf_exempt
def employee(request, id, edit) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    target = Employee.objects.filter(id=id).first()
    params = {
        'title' : 'Employee',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'id' : id,
        'edit' : edit,
        'form' : EmployeeForm(instance=target)
    }
    if edit == 2 :
        params['msg'] = '本当に削除しますか？'
    elif edit == 4 :
        target = Shipper.objects.filter(id=id)
        target.delete()
        return redirect('show_shipper')
    elif request.POST :
        form = EmployeeForm(data=request.POST)
        if form.is_valid() :
            if edit == 5 :
                params['msg'] = 'この内容で更新してよいですか？'
                params['form'] = form
            elif edit == 3 :
                form.instance.id = id
                form.save()
                return redirect('show_employees')
        else :
            errors = form.errors.as_data()
            for field_name, field_errors in errors.items():
                print(f"Field '{field_name}':")
                for error in field_errors:
                    print(f"- {error}")
            params['msg'] = '入力に誤りがあります'
        params['form'] = form
    return render(request, 'employee.html', params)

@csrf_exempt
def add_employee(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'New Employee',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'form' : AddEmployeeForm(),
    }
    if request.POST :
        form = AddEmployeeForm(data=request.POST)
        if form.is_valid() :
            if not request.session['add_employee_confirm'] :
                if Employee.objects.filter(phone=request.POST['phone']).count() > 0 :
                    if request.POST['auth'] :
                        params['msg'] = '既に登録されている管理者電話番号です'
                    else :
                        params['msg'] = '既に登録されているドライバー電話番号です'
                else :
                    request.session['add_employee_confirm'] = True
                    params['msg'] = 'この内容で登録します、よろしいですか？'
                    data = request.POST.copy()
                    data.update({'dummy':request.POST['phone']})
                    form = AddEmployeeForm(data=data)
            else :
                form.instance.password = request.POST['phone']
                form.instance.save()
                del request.session['add_employee_confirm']
                return redirect('show_employees')
        else :
            params['msg'] = '入力に誤りがあります'
        params['form'] = form
        params['password'] = request.POST['phone']
    else :
        request.session['add_employee_confirm'] = False
        params['msg'] = 'ドライバーもしくは管理者を登録できます'
        params['password'] = ""
    return render(request, 'add_employee.html', params)

@csrf_exempt
def add_file(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Upload',
        'msg' : 'PDFファイルをアップロードできます',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'form' : UploadForm(),
    }
    if request.POST :
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid() :
            consignee = Consignee.objects.filter(id=form.cleaned_data['consignee']).first()
            form.instance.consignee = consignee
            form.save()
            return redirect('show_files')
        else :
            params['msg'] = '入力に誤りがあります'
    return render(request, 'add_file.html', params)

@csrf_exempt
def show_files(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Files',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'list' : File.objects.all(),
    }
    return render(request, 'show_files.html', params)

@csrf_exempt
def del_file(request, id) :
    for file in File.objects.filter(id=id) :
        file.delete()
    return redirect('show_files')

@csrf_exempt
def show_organization(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Organizations',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'list' : Organization.objects.all(),
    }
    return render(request, 'show_organization.html', params)

@csrf_exempt
def organization(request, id, edit) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    target = Organization.objects.filter(id=id).first()
    params = {
        'title' : 'Organization',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'id' : id,
        'edit' : edit,
        'form' : OrganizationForm(instance=target),
        'employees' : Employee.objects.filter(organization=id).all()
    }
    if request.POST :
        form = OrganizationForm(data=request.POST)
        if edit == 1 :
            if form.is_valid() :
                params['msg'] = 'この内容で更新してよいですか？'
                params['form'] = form
            else :
                params['msg'] = '入力に誤りがあります'
        elif edit == 3 :
            target.name = request.POST['name']
            target.kana = request.POST['kana']
            target.save()
            return redirect('show_organization')
    else :
        if edit == 2 :
            params['msg'] = '所属従業員のデータも同時に削除されますが、本当に削除しますか？'
        elif edit == 4 :
            target = Organization.objects.filter(id=id)
            target.delete()
            return redirect('show_organization')
    return render(request, 'organization.html', params)

@csrf_exempt
def add_organization(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'New Organization',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'form' : OrganizationForm(),
    }
    if request.POST :
        form = OrganizationForm(data=request.POST)
        if form.is_valid() :
            if not request.session['add_organization_confirm'] :
                request.session['add_organization_confirm'] = True
                params['msg'] = 'この内容で登録します、よろしいですか？'
            else :
                form.instance.save()
                del request.session['add_organization_confirm']
                return redirect('show_organization')
        else :
            del params['disable']
            params['msg'] = '入力に誤りがあります'
        params['form'] = form
    else :
        request.session['add_organization_confirm'] = False
        params['msg'] = '部署を登録できます'
    return render(request, 'add_organization.html', params)

@csrf_exempt
def show_shipper(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Makers(Shippers)',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'list' : Shipper.objects.all(),
    }
    return render(request, 'show_shipper.html', params)

@csrf_exempt
def shipper(request, id, edit) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    target = Shipper.objects.filter(id=id).first()
    params = {
        'title' : 'Maker(Shipper)',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'id' : id,
        'edit' : edit,
        'form' : ShipperForm(instance=target),
        'consignees' : Consignee.objects.filter(shipper=id).all()
    }
    if edit == 2 :
        params['msg'] = '本当に削除しますか？'
    elif edit == 4 :
        target = Shipper.objects.filter(id=id)
        target.delete()
        return redirect('show_shipper')
    elif request.POST :
        form = ShipperForm(data=request.POST)
        if form.is_valid() :
            if edit == 5 :
                params['msg'] = 'この内容で更新してよいですか？'
                params['form'] = form
            elif edit == 3 :
                form.instance.id = id
                form.save()
                return redirect('show_shipper')
        else :
            errors = form.errors.as_data()
            for field_name, field_errors in errors.items():
                print(f"Field '{field_name}':")
                for error in field_errors:
                    print(f"- {error}")
            params['msg'] = '入力に誤りがあります'
        params['form'] = form
    return render(request, 'shipper.html', params)

@csrf_exempt
def add_shipper(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'New Maker(Shipper)',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'form' : ShipperForm(),
    }
    if request.POST :
        form = ShipperForm(data=request.POST)
        if form.is_valid() :
            if not request.session['add_shipper_confirm'] :
                request.session['add_shipper_confirm'] = True
                params['msg'] = 'この内容で登録します、よろしいですか？'
            else :
                form.instance.save()
                del request.session['add_shipper_confirm']
                return redirect('show_shipper')
        else :
            del params['disable']
            params['msg'] = '入力に誤りがあります'
        params['form'] = form
    else :
        request.session['add_shipper_confirm'] = False
        params['msg'] = 'メーカー(荷主)を登録できます'
    return render(request, 'add_shipper.html', params)

@csrf_exempt
def show_consignee(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'Consignees',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'list' : Consignee.objects.all(),
    }
    return render(request, 'show_consignee.html', params)

@csrf_exempt
def consignee(request, id, edit) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    target = Consignee.objects.filter(id=id).first()
    form = ConsigneeForm(instance=target)
    form.fields['prefecture'].initial = target.city.prefecture.id
    form.fields['city'].initial = target.city.id
    params = {
        'title' : 'Consignee',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
        'id' : id,
        'edit' : edit,
        'form' : form,
        'model' : target,
        'city_selected' : target.city.id,
        'city_list' : get_city_select(target.city.prefecture.id)
    }
    if edit == 2 :
        params['msg'] = '本当に削除しますか？'
    elif edit == 4 :
        target = Consignee.objects.filter(id=id)
        target.delete()
        return redirect('show_consignee')
    elif request.POST :
        form = ConsigneeForm(data=request.POST)
        if request.POST['prefecture'] :
            form.fields['prefecture'].initial = request.POST['prefecture']
            params['city_list'] = get_city_select(request.POST['prefecture'])
            if request.POST["city"] :
                form.fields['city'].initial = request.POST["city"]
                params['city_selected'] = int(request.POST["city"])
        if form.is_valid() :
            if edit == 5 :
                params['msg'] = 'この内容で更新してよいですか？'
            else :
                form.instance.id = id
                form.instance.city = City.objects.filter(id=form.cleaned_data['city']).first()
                form.save()
                return redirect('show_consignee')
        else :
            errors = form.errors.as_data()
            for field_name, field_errors in errors.items():
                print(f"Field '{field_name}':")
                for error in field_errors:
                    print(f"- {error}")
            params['msg'] = '入力に誤りがあります'
        params['form'] = form
    return render(request, 'consignee.html', params)

@csrf_exempt
def add_consignee(request) :
    employee = get_employee(request, True)
    if not employee :
        return redirect('admin_login')
    params = {
        'title' : 'New Consignee',
        'msg' : '',
        'name' : employee.name,
        'organizaion' : employee.organization.name,
    }
    if request.POST :
        params['city_selected'] = int(request.POST["city"])
        params['city_list'] = get_city_select(request.POST['prefecture'])
        form = ConsigneeForm(data=request.POST)
        if form.is_valid() :
            if not request.session['add_consignee_confirm'] :
                request.session['add_consignee_confirm'] = True
                params['msg'] = 'この内容で登録します、よろしいですか？'
                params['form'] = form
            else :
                form.instance.city = City.objects.filter(id=form.cleaned_data['city']).first()
                form.save()
                del request.session['add_consignee_confirm']
                return redirect('show_consignee')
        else :
            errors = form.errors.as_data()
            for field_name, field_errors in errors.items():
                print(f"Field '{field_name}':")
                for error in field_errors:
                    print(f"- {error}")
            params['msg'] = '入力に誤りがあります'
            params['form'] = form
    else :
        request.session['add_consignee_confirm'] = False
        params['msg'] = '納品先を登録できます'
        params['form'] = ConsigneeForm()
    return render(request, 'add_consignee.html', params)

@csrf_exempt
def get_cities(request) :
    prefecture_id = request.GET.get('prefecture_id')
    return JsonResponse({'cities': get_city_select(prefecture_id)})

def get_employee(request, auth_flg) :
    if not 'employee' in request.session :
        return None
    employee = Employee.objects.filter(id=request.session['employee']).first()
    if not employee :
        return None
    if auth_flg and not employee.auth :
        return None
    return employee

def get_city_select(prefecture_id) :
    cities = City.objects.filter(prefecture_id=prefecture_id).order_by('id')
    city_list = []
    for city in cities:
        city_list.append({'id': city.id, 'name': city.name})
    return city_list

def get_consignees(request) :
    city_id = request.GET.get('city_id')
    return JsonResponse({'consignees': get_consignee_select(city_id)})

def get_consignee_select(city_id) :
    consignees = Consignee.objects.filter(city_id=city_id).order_by('id')
    consignee_list = []
    for consignee in consignees:
        consignee_list.append({'id': consignee.id, 'name': consignee.name})
    return consignee_list

def get_consignees_from_shipper(request) :
    shipper_id = request.GET.get('shipper_id')
    consignees = Consignee.objects.filter(shipper_id=shipper_id).order_by('id')
    consignee_list = []
    for consignee in consignees:
        consignee_list.append({'id': consignee.id, 'name': consignee.name})
    return JsonResponse({'consignees': consignee_list})

def get_phone(request) :
    consignee_id = request.GET.get('consignee_id')
    print(consignee_id)
    phone = Consignee.objects.filter(id=consignee_id).first().phone
    return JsonResponse({'phone': phone})

