from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from myproject import models
from myproject.utils.encrypt import md5


class LoginForm(forms.Form):
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"}),
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"}, render_value=True),
        required=True
    )

    userType = forms.ChoiceField(
        label="用户类型",
        choices=(
            (1, "医院"),
            (2, "保险公司"),
            (3, "医药供应商"),
            (4, "医疗设备供应商"),
            (5, "管理员"),
        ),
    )

    def clean_password(self):
        # 获取数据传入密码，进行md5加密 返回加密后的值 与数据库中的数据进行校验
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class RegisterForm(forms.Form):
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"}),
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"}, render_value=True),
        required=True
    )
    userType = forms.ChoiceField(
        label="用户类型",
        choices=(
            (1, "医院"),
            (2, "保险公司"),
            (3, "医药供应商"),
            (4, "医疗设备供应商"),
            (5, "管理员"),
        )
    )


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "confirm_password", "userType"]

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
            raise ValidationError("用户已存在")

        return txt_name

    def clean_password(self):
        # 获取数据传入密码，进行md5加密 返回加密后的值 与数据库中的数据进行校验
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")

        return confirm


def clean_password(self):
    # 获取数据传入密码，进行md5加密 返回加密后的值 与数据库中的数据进行校验
    pwd = self.cleaned_data.get("password")
    return md5(pwd)


# 登录
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        request.session["info"] = {"id": user_object.id, "name": user_object.name, "userType": user_object.userType}
        num = form.data.get("userType")
        if num == '1':
            return redirect('/hospital/list')
        elif num == '2':
            return redirect('/insurance/list')
        elif num == '3':
            return redirect('/drogs_company/list')
        elif num == '4':
            return redirect('/devices_company/list')
        elif num == '5':
            return redirect('/manageadmin')

    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        name = form.data.get("name")
        num = form.data.get("userType")
        password = form.data.get("password")
        if num == '1':
            models.hospital.objects.create(name=name, password=md5(password))
        elif num == '2':
            models.insurance_company.objects.create(name=name, password=md5(password))
        elif num == '3':
            models.drogs_company.objects.create(name=name, password=md5(password))
        elif num == '4':
            models.devices_company.objects.create(name=name, password=md5(password))
        elif num == '5':
            models.AdminInfo.objects.create(name=name, password=md5(password))
        return redirect('/login')

    return render(request, 'register.html', {'form': form})