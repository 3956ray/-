from django import forms
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect


# Create your views here.
###科室处理###
from myproject import models
from myproject.utils.pagenation import Pagenation


class DepartmentModelForm(forms.ModelForm):
    name = forms.CharField(
        label="科室名称",
        validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.department
        fields = ["name", "hospital"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # def clean_name(self):
    #     txt_name = self.cleaned_data["name"]
    #     # txt_province = self.cleaned_data["province"]
    #     exists_name = models.department.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
    #     # exists_province = models.hospital.objects.filter(name=txt_province).exists()
    #     # 当前编辑得那一行
    #
    #     if exists_name:
    #         raise ValidationError("科室已存在")
    #
    #     return txt_name


# 科室列表
def department_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 获取科室数据
    list = models.department.objects.filter(**data_dict).order_by("id")
    page_object = Pagenation(request, list)
    context = {
        'search_data': search_data,
        'list': page_object.page_list,
        'page_string': page_object.html()
    }
    return render(request, 'hospital/department/department_list.html', context)


# 科室添加
def department_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = DepartmentModelForm()
        return render(request, 'hospital/department/department_add.html', {'form': form})

    # 获取用户提交的数据
    form = DepartmentModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/hospital/department/")
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/department/department_add.html', {'form': form})


# 科室编辑
def department_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.department.objects.filter(id=nid).first()
    if request.method == "GET":
        form = DepartmentModelForm(instance=list)
        return render(request, 'hospital/department/department_edit.html', {'form': form})

    form = DepartmentModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()

        # 获取药品数量,并更新数据库
        num = models.drogs.objects.filter(department=nid).count()
        models.department.objects.filter(id=nid).update(drogsNumber=num)
        # 获取设备数量
        num = models.devicecs.objects.filter(department=nid).count()
        models.department.objects.filter(id=nid).update(devicesNumber=num)
        # 获取患者数量
        num = models.patient_history.objects.filter(department=nid).count()
        models.department.objects.filter(id=nid).update(patientNumber=num)
        return redirect('/hospital/department')
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/department/department_edit.html', {'form': form})


# 科室删除
def department_delete(request):
    nid = request.GET.get('nid')
    models.department.objects.filter(id=nid).delete()
    return redirect('/hospital/department')