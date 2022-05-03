from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect

# Create your views here.

###医药公司处理###
from myproject import models
from myproject.utils.pagenation import Pagenation


class DrogsCompanyModelForm(forms.ModelForm):
    name = forms.CharField(
        label="医药公司名称",
        # validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.drogs_company
        fields = ["name", "password", "drogsProvideNumber", "drogsQuality"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists_name = models.drogs_company.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()

        if exists_name:
            raise ValidationError("公司已存在")

        return txt_name


# 医药公司用户列表
def drogs_company_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.drogs_company.objects.filter(**data_dict).order_by("id")
    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'drogs_company/drogs_company_list.html', context)


# 医药公司添加
def drogs_company_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = DrogsCompanyModelForm()
        return render(request, 'drogs_company/drogs_company_add.html', {'form': form})

    # 获取用户提交的数据
    form = DrogsCompanyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/drogs_company/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'drogs_company/drogs_company_add.html', {'form': form})


# 医药公司编辑
def drogs_company_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.drogs_company.objects.filter(id=nid).first()
    if request.method == "GET":
        form = DrogsCompanyModelForm(instance=list)
        return render(request, 'drogs_company/drogs_company_edit.html', {'form': form})

    form = DrogsCompanyModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()

        # 获取提供医药数量,并更新数据库
        num = models.drogs_provide.objects.filter(drogs_company=nid).count()
        models.drogs_company.objects.filter(id=nid).update(drogsProvideNumber=num)
        # print(num)
        return redirect("/drogs_company/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'drogs_company/drogs_company_edit.html', {'form': form})


# 医药公司删除
def drogs_company_delete(request):
    nid = request.GET.get('nid')
    models.drogs_company.objects.filter(id=nid).delete()
    return redirect("/drogs_company/list")


###药品处理###
class DrogsProvideModelForm(forms.ModelForm):
    name = forms.CharField(
        label="药品名称",
        validators=[RegexValidator(r'^[\u4e00-\u9fa5a-zA-Z]+$', '请填写中文或是英文')]
    )

    class Meta:
        model = models.drogs_provide
        fields = ["name", "amount", "drogs_company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class = "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists_name = models.drogs_provide.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()

        if exists_name:
            raise ValidationError("已存在")

        return txt_name


# 医药公司用户列表
def drogs_provide_list(request):
    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    list = models.drogs_provide.objects.filter(**data_dict).order_by("id")

    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'drogs_company/drogs_provide/drogs_provide_list.html', context)


# 医药公司添加
def drogs_provide_add(request):
    if request.method == "GET":
        # 使用modelform生成前端
        form = DrogsProvideModelForm()
        return render(request, 'drogs_company/drogs_provide/drogs_provide_add.html', {'form': form})

    # 获取用户提交的数据
    form = DrogsProvideModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/drogs_company/drogs_provide/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'drogs_company/drogs_provide/drogs_provide_add.html', {'form': form})


# 医药公司编辑
def drogs_provide_edit(request, nid):
    # 根据ID 获取需要编辑得那行数据 list类型(object)
    list = models.drogs_provide.objects.filter(id=nid).first()
    if request.method == "GET":
        form = DrogsProvideModelForm(instance=list)
        return render(request, 'drogs_company/drogs_provide/drogs_provide_edit.html', {'form': form})

    form = DrogsProvideModelForm(data=request.POST, instance=list)
    if form.is_valid():
        form.save()
        return redirect("/drogs/drogs_provide/list")
    else:
        # 校验失败，显示错误信息
        return render(request, 'drogs_company/drogs_provide/drogs_provide_edit.html', {'form': form})


# 医药公司删除
def drogs_provide_delete(request):
    nid = request.GET.get('nid')
    models.drogs_provide.objects.filter(id=nid).delete()
    return redirect("/drogs_company/drogs_provide/list")


def drogs_provide_user_edit(request, nid):
    list = models.drogs_provide.objects.filter(drogs_company_id=nid).order_by("id")
    page_object = Pagenation(request, list)
    context = {
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }
    # 寻找医院以及保险科室交集
    # 通过交集 找到属于该病院的患者
    # print(queryset3.)
    return render(request, 'drogs_company/drogs_company_user_list.html', context)


def drogs_provide_evaluate(request, nid):  # 传入空字典
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
    return render(request, 'drogs_company/drogs_company_evaluate.html', context)


def drogs_provide_evaluate_list(request, nid, eid):
    '''
    :param request:
    :param nid: 选择的医院
    :param eid: 选择的医药公司
    :return:
    '''
    # 获取该公司的药品
    q1 = models.drogs_provide.objects.filter(drogs_company_id=eid).values('name')
    # 初始化字典
    # 直接在里头存放该医药公司之药品，并初始化值为0
    d = {}
    for i in q1:
        name = i.get('name')
        # 初始化字典
        d[name] = 0

    # 获取对象医院科室数据
    q2 = models.department.objects.filter(hospital=nid).values('id')
    # 获取该科室之下的所有药品
    for i in q2:
        # 根据id逐个查询科室药品
        drogID = i.get('id')
        q3 = models.drogs.objects.filter(department_id=drogID).values('name')
        print(q3)
        # 查到一条数据 药品是否在字典当中 若是有则药品+1，若无跳过
        for j in q3:
            name = j.get('name')
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
    drogs_company_name = models.drogs_company.objects.filter(id=eid).values('name').get().get('name')
    hospital_name = models.hospital.objects.filter(id=nid).values('name').get().get('name')
    print("医药公司："+drogs_company_name + "\n医院:"+hospital_name)

    # 检验是否已经存在数据库当中,若存在更新分数，不存在则新增
    flag = models.drogs_company_evaluate.objects.filter(drogs_company_name=drogs_company_name, hospital_name=hospital_name)
    if flag:
        flag.update(score=score)
    else:
        models.drogs_company_evaluate.objects.create(drogs_company_name=drogs_company_name, hospital_name=hospital_name,
                                                 score=score)

    # 传入空字典
    data_dict = {}
    # 获取搜索字段
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["insurance_name__contains"] = search_data

    list = models.drogs_company_evaluate.objects.filter(**data_dict).order_by("id")

    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html(),  # 页码
    }
    return render(request, 'drogs_company/drogs_company_evaluate_list.html', context)
