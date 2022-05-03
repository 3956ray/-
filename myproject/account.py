from django import forms
from django.shortcuts import render

from myproject import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = models.AdminInfo
        fields = ["name", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def login(request):
    a = LoginForm()
    context = {
        'aform': a
    }
    return render(request, 'admin/admin_add.html', context)
