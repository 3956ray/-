from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.utils.safestring import mark_safe

from myproject import models
from myproject.models import UserInfo

from myproject.utils.pagenation import Pagenation
from myproject.utils.encrypt import md5


# 显示用户列表
def user_list(request):
    # models.UserInfo.objects.create(name="rice", password="123", userType="npy")
    # models.UserInfo.objects.create(name="cyj", password="123", userType="npy")

    # models.UserInfo.objects.filter(name="rice").delete()
    data_list = models.UserInfo.objects.all();
    return render(request, 'user/user_list.html', {"data_list": data_list})


# 显示用户信息
def user_info(request):
    return render(request, 'user/user_info.html')


# 用户添加
def user_add(request):
    # 先获取添加页面
    if request.method == "GET":
        return render(request, 'user/user_add.html')
    # 获取用户提交的数据
    name = request.POST.get("user")
    password = request.POST.get("password")
    userType = request.POST.get("userType")

    # 添加到数据库
    UserInfo.objects.create(name=name, password=password, userType=userType)
    return redirect("/user/list")


def user_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")


###管理员处理###

class AdminModelForm(forms.ModelForm):
    name = forms.CharField(
        label="管理员名称",
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.AdminInfo
        fields = ["name", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists_name = models.AdminInfo.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        # 当前编辑得那一行

        if exists_name:
            raise ValidationError("管理员已存在")

        return txt_name

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")

        return confirm


# 管理员编辑ModelForm
class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model = models.AdminInfo
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists_name = models.AdminInfo.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        # 当前编辑得那一行

        if exists_name:
            raise ValidationError("管理员已存在")

        return txt_name


# 管理员重置密码ModelForm
class AdminPwdMResetModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.AdminInfo
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")

        return confirm


def admin_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.AdminInfo.objects.filter(**data_dict).order_by("id")

    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }
    return render(request, 'admin/admin_list.html', context)


def admin_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = AdminModelForm()
        return render(request, 'admin/admin_add.html', {'form': form})

    # 获取用户提交的数据
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/manageadmin")
    else:
        # 校验失败，显示错误信息
        return render(request, 'admin/admin_add.html', {'form': form})


def admin_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.AdminInfo.objects.filter(id=nid).first()
    title = list.name
    if request.method == "GET":
        form = AdminEditModelForm(instance=list)
        return render(request, 'admin/admin_reset.html', {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()
        return redirect("/manageadmin")
    else:
        # 校验失败，显示错误信息
        return render(request, 'admin/admin_reset.html', {'form': form})


# 重置密码
def admin_pwd_reset(request, nid):
    list = models.AdminInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminPwdMResetModelForm()
        return render(request, 'admin/admin_edit.html', {'form': form})

    form = AdminPwdMResetModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()
        return redirect("/manageadmin")
    else:
        # 校验失败，显示错误信息
        return render(request, 'admin/admin_edit.html', {'form': form})


def admin_delete(request):
    nid = request.GET.get('nid')
    models.AdminInfo.objects.filter(id=nid).delete()
    return redirect("/manageadmin")


###医院处理###

class HospitalModelForm(forms.ModelForm):
    name = forms.CharField(
        label="医院名称",
        # validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.hospital
        fields = ["name", "password", "province", "departmentNumber"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        # txt_province = self.cleaned_data["province"]
        exists_name = models.hospital.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        # exists_province = models.hospital.objects.filter(name=txt_province).exists()
        # 当前编辑得那一行

        if exists_name:
            raise ValidationError("医院已存在")

        return txt_name


# 医院用户列表
def hospital_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.hospital.objects.filter(**data_dict).order_by("id")

    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'hospital/hospital_list.html', context)


# 医院添加
def hospital_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = HospitalModelForm()
        return render(request, 'hospital/hospital_add.html', {'form': form})

    # 获取用户提交的数据
    form = HospitalModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/hospital/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/hospital_add.html', {'form': form})


# 医院编辑
def hospital_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.hospital.objects.filter(id=nid).first()
    if request.method == "GET":
        form = HospitalModelForm(instance=list)
        return render(request, 'hospital/hospital_edit.html', {'form': form})

    form = HospitalModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()

        # 获取科室数量,并更新数据库
        num = models.department.objects.filter(hospital=nid).count()
        models.hospital.objects.filter(id=nid).update(departmentNumber=num)
        # print(num)
        return redirect("/hospital/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/hospital_edit.html', {'form': form})


# 医院删除
def hospital_delete(request):
    nid = request.GET.get('nid')
    models.hospital.objects.filter(id=nid).delete()
    return redirect("/hospital/list")


###药品处理###
class DrogsModelForm(forms.ModelForm):
    name = forms.CharField(
        label="药品名称",
        validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.drogs
        fields = ["name", "department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists_name = models.drogs.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()

        if exists_name:
            raise ValidationError("药品已存在")

        return txt_name


# 药品列表
def drogs_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.drogs.objects.filter(**data_dict).order_by("id")
    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'hospital/department/drogs/drogs_list.html', context)


# 医药公司添加
def drogs_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = DrogsModelForm()
        return render(request, 'hospital/department/drogs/drogs_add.html', {'form': form})

    # 获取用户提交的数据
    form = DrogsModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/hospital/department/drogs/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/department/drogs/drogs_add.html', {'form': form})


# 医药公司编辑
def drogs_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.drogs.objects.filter(id=nid).first()
    if request.method == "GET":
        form = DrogsModelForm(instance=list)
        return render(request, 'hospital/department/drogs/drogs_edit.html', {'form': form})

    form = DrogsModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()

        return redirect("/hospital/department/drogs/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/department/drogs/drogs_edit.html', {'form': form})


# 医药公司删除
def drogs_delete(request):
    nid = request.GET.get('nid')
    models.drogs.objects.filter(id=nid).delete()
    return redirect("/hospital/department/drogs/list")


###设备处理###
class DevicesModelForm(forms.ModelForm):
    name = forms.CharField(
        label="设备名称",
        validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.devicecs
        fields = ["name", "department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists_name = models.devicecs.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()

        if exists_name:
            raise ValidationError("设备已存在")

        return txt_name


# 药品列表
def devices_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.devicecs.objects.filter(**data_dict).order_by("id")
    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'hospital/department/devices/devices_list.html', context)


# 设备公司添加
def devices_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = DevicesModelForm()
        return render(request, 'hospital/department/devices/devices_add.html', {'form': form})

    # 获取用户提交的数据
    form = DevicesModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/hospital/department/devices/list/")
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/department/devices/devices_add.html', {'form': form})


# 设备公司编辑
def devices_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.devicecs.objects.filter(id=nid).first()
    if request.method == "GET":
        form = DrogsModelForm(instance=list)
        return render(request, 'hospital/department/devices/devices_edit.html', {'form': form})

    form = DrogsModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()

        # print(num)
        return redirect("/hospital/department/devices")
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/department/devices/devices_edit.html', {'form': form})


# 设备公司删除
def devices_delete(request):
    nid = request.GET.get('nid')
    models.devicecs.objects.filter(id=nid).delete()
    return redirect("/hospital/department/devices/list")


def home(request):
    return render(request, 'home.html')
