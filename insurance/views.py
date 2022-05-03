from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models.sql import AND
from django.shortcuts import render, redirect

# Create your views here.

###保险公司处理###
from myproject import models
# from insurance import models
from myproject.utils.pagenation import Pagenation


class InsuranceCompanyModelForm(forms.ModelForm):
    name = forms.CharField(
        label="保险公司名称",
        # validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.insurance_company
        fields = ["name", "password", "insuranceProvideNumber"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists_name = models.insurance_company.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()

        if exists_name:
            raise ValidationError("公司已存在")

        return txt_name


# 保险公司用户列表
def insurance_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.insurance_company.objects.filter(**data_dict).order_by("id")
    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'insurance/insurance_list.html', context)


# 保险公司添加
def insurance_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = InsuranceCompanyModelForm()
        return render(request, 'insurance/insurance_add.html', {'form': form})

    # 获取用户提交的数据
    form = InsuranceCompanyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/insurance/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'insurance/insurance_add.html', {'form': form})


# 保险公司编辑
def insurance_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.insurance_company.objects.filter(id=nid).first()
    if request.method == "GET":
        form = InsuranceCompanyModelForm(instance=list)
        return render(request, 'insurance/insurance_edit.html', {'form': form})

    form = InsuranceCompanyModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()

        # 获取提供保险数量,并更新数据库
        num = models.insurance_provide.objects.filter(insurance_company=nid).count()
        models.insurance_company.objects.filter(id=nid).update(insuranceProvideNumber=num)
        # print(num)
        return redirect("/insurance/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'insurance/insurance_edit.html', {'form': form})


# 保险公司删除
def insurance_delete(request):
    nid = request.GET.get('nid')
    models.insurance_company.objects.filter(id=nid).delete()
    return redirect("/insurance/list")


###保险处理###
class InsuranceProvideModelForm(forms.ModelForm):
    name = forms.CharField(
        label="保险名称",
        validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.insurance_provide
        fields = ["name", "amount", "insurance_company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


# 保险公司用户列表
def insurance_provide_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.insurance_provide.objects.filter(**data_dict).order_by("id")
    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'insurance/insurance_provide/insurance_provide_list.html', context)


# 保险公司添加
def insurance_provide_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = InsuranceProvideModelForm()
        return render(request, 'insurance/insurance_provide/insurance_provide_add.html', {'form': form})

    # 获取用户提交的数据
    form = InsuranceProvideModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/insurance/insurance_provide/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'insurance/insurance_provide/insurance_provide_add.html', {'form': form})


# 保险公司编辑
def insurance_provide_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.insurance_provide.objects.filter(id=nid).first()
    if request.method == "GET":
        form = InsuranceProvideModelForm(instance=list)
        return render(request, 'insurance/insurance_provide/insurance_provide_edit.html', {'form': form})

    form = InsuranceProvideModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()
        return redirect("/insurance/insurance_provide/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'insurance/insurance_provide/insurance_provide_edit.html', {'form': form})


# 保险公司删除
def insurance_provide_delete(request):
    nid = request.GET.get('nid')
    models.insurance_provide.objects.filter(id=nid).delete()
    return redirect("/insurance/insurance_provide/list")


def insurance_user_list(request, nid):
    list = models.insurance_provide.objects.filter(insurance_company_id=nid).order_by("id")
    page_object = Pagenation(request, list)
    context = {
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }
    # 寻找医院以及保险科室交集
    # 通过交集 找到属于该病院的患者
    # print(queryset3.)
    return render(request, 'insurance/insurance_user_list.html', context)


def insurance_evaluate(request, nid):
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
        'page_string': page_object.html(),  # 页码
        'nid': nid
    }

    return render(request, 'insurance/insurance_evaluate.html', context)


def insurance_evaluate_list(request, nid, eid):
    '''
    :param request:
    :param nid: 选择的医院
    :param eid: 选择的公司
    :return:
    '''
    # 获取该公司的保险
    q1 = models.insurance_provide.objects.filter(insurance_company_id=eid).values('name')
    # 获取对象医院科室数据
    q2 = models.department.objects.filter(hospital=nid)
    # 获取保险以及对象的科室交集
    intersection = q1.intersection(q2.values('name'))
    # 获取该医院病人数据, 使用values拿到所有病人id
    q3 = models.patient.objects.filter(hospital=nid).values('id')

    # 空字典 存放交集数据
    # key = 交集， value = 人数
    d = {}
    for i in intersection:
        name = i.get('name')
        # 初始化字典
        d[name] = 0

    for i in q3:
        # 根据id逐个查询患者病史
        pahis = i.get('id')
        # 获取该患者病史
        q4 = models.patient_history.objects.filter(patient_id=pahis).values('dexcribe')
        print(q4)
        # 查到一条数据 检查科室是否存在于字典当中，若存在 该科室值+1
        for j in q4:
            name = j.get('dexcribe')
            print(type(name))
            if name in d:
                d[name] = d[name] + 1
            else:
                print(name + "不在字典当中")
            print(d)
    # 初始化评估分数
    score = 0
    for key in d:
        score = d[key] + score
    print("score:" + str(score))

    # 保存数据
    insurance_name = models.insurance_company.objects.filter(id=eid).values('name').get().get('name')
    hospital_name = models.hospital.objects.filter(id=nid).values('name').get().get('name')
    print("保险公司:"+insurance_name + "\n医院:"+hospital_name)

    # 检验是否已经存在数据库当中,若存在更新分数，不存在则新增
    flag = models.insurance_evaluate.objects.filter(insurance_name=insurance_name, hospital_name=hospital_name)
    if flag:
        flag.update(score=score)
    else:
        models.insurance_evaluate.objects.create(insurance_name=insurance_name, hospital_name=hospital_name,
                                                 score=score)

    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["insurance_name__contains"] = search_data

    list = models.insurance_evaluate.objects.filter(**data_dict).order_by("id")

    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html(),  # 页码
    }
    return render(request, 'insurance/insurance_evaluate_list.html', context)


# def insurance_evaluate_delete(request):
#     nid = request.GET.get('nid')
#     models.insurance_provide.objects.filter(id=nid).delete()
#     return redirect("/insurance/insurance_provide/list")
