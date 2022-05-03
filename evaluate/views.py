from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
# Create your views here.
from myproject.utils.pagenation import Pagenation
from myproject import models


def evaluate_insurance(request):
    data_dict = {}
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
    return render(request, 'evaluate/evaluate_insurance.html', context)

def count_insurance():

    # 拿到医院病人总数
    # 每有一个病人的一分

    return
