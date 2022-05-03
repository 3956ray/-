from django import forms
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect


# Create your views here.

###患者处理###
# 患者列表
from myproject import models
from myproject.utils.pagenation import Pagenation


def patient_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 获取患者数据
    list = models.patient.objects.filter(**data_dict).order_by("id")
    page_object = Pagenation(request, list)
    context = {
        'search_data': search_data,
        'list': page_object.page_list,
        'page_string': page_object.html()
    }

    return render(request, 'hospital/patient/patient_list.html', context)


# 患者ModelForm
class PatientModelForm(forms.ModelForm):
    name = forms.CharField(
        label="姓名",
        validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )
    age = forms.IntegerField(
        label="年龄",
        validators=[RegexValidator(r'^[+]{0,1}(\d+)$', '年龄不能小于0')]
    )

    class Meta:
        model = models.patient
        fields = ["name", "birthday", "age", "gender", "hospital"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


# 患者历史ModelForm
class PatientHistoryModelForm(forms.ModelForm):
    # patient = forms.CharField(disabled=True)

    dexcribe = forms.CharField(
        label="病史描述",
        validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.patient_history
        fields = ["patient", "department", "dexcribe"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


# 患者添加
def patient_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = PatientModelForm()
        return render(request, 'hospital/patient/patient_add.html', {'form': form})

    # 获取用户提交的数据
    form = PatientModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/hospital/patient')
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/patient/patient_add.html', {'form': form})


# 患者编辑
def patient_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.patient.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PatientModelForm(instance=list)
        return render(request, 'hospital/patient/patient_edit.html', {'form': form})

    form = PatientModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()
        return redirect('/hospital/patient')
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/patient/patient_edit.html', {'form': form})


# 患者删除
def patient_delete(request):
    nid = request.GET.get('nid')
    models.patient.objects.filter(id=nid).delete()
    return redirect('/hospital/patient')


# 患者病史
def patient_history_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    # 获取患者数据
    list = models.patient_history.objects.filter(**data_dict).order_by("id")

    page_object = Pagenation(request, list)
    context = {
        'search_data': search_data,
        'list': page_object.page_list,
        'page_string': page_object.html()
    }
    return render(request, 'hospital/patient/patient_history_list.html', context)


# 患者病史添加
def patient_history_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = PatientHistoryModelForm()
        return render(request, 'hospital/patient/patient_history_add.html', {'form': form})

    # 获取用户提交的数据
    form = PatientHistoryModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/hospital/patient/history')
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/patient/patient_history_add.html', {'form': form})


def patient_history_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.patient_history.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PatientHistoryModelForm(instance=list)
        return render(request, 'hospital/patient/patient_history_edit.html', {'form': form})

    form = PatientHistoryModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()
        return redirect('/hospital/patient/history')
    else:
        # 校验失败，显示错误信息
        return render(request, 'hospital/patient/patient_history_edit.html', {'form': form})


# 患者病史删除
def patient_history_delete(request):
    nid = request.GET.get('nid')
    models.patient_history.objects.filter(id=nid).delete()
    return redirect('/hospital/patient/history')

def patient_user_list(request, nid):
    list = models.patient_history.objects.filter(patient_id=nid).order_by("id")
    page_object = Pagenation(request, list)
    context = {
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }
    return render(request, 'hospital/patient/patient_history_user_list.html', context)