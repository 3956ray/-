from django.db import models


# Create your models here.
# 在新增列时，由于已经存在列中可能已有数据，所以新增列必须要指定新增列对应的数据
# 1.手动输入一个值
# 2.default=值
# 3.设置为空 null=True, blank=True
# 再执行命令
# python manage.py makemigrations
# python manage.py migrate

class AdminInfo(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)


class UserInfo(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    userType_choices = {
        (1, "医院"),
        (2, "保险公司"),
        (3, "医药供应商"),
        (4, "医疗设备供应商"),
        (5, "管理员"),
    }
    userType = models.SmallIntegerField(verbose_name="用户种类", max_length=32, choices=userType_choices)

    def __str__(self):
        return self.name


class hospital(models.Model):
    # 医院信息
    name = models.CharField(verbose_name="医院名称", max_length=32)
    password = models.CharField(verbose_name="医院密码", max_length=64)

    # 中国省份
    province_choices = {
        (1, "安徽"),
        (2, "北京"),
        (3, "重庆"),
        (4, "福建"),
        (5, "甘肃"),
        (6, "广东"),
        (7, "广西"),
        (8, "贵州"),
        (9, "海南"),
        (10, "河北"),
        (11, "河南"),
        (12, "黑龙江"),
        (13, "湖北"),
        (14, "湖南"),
        (15, "吉林"),
        (16, "江苏"),
        (17, "江西"),
        (18, "辽宁"),
        (19, "内蒙古"),
        (20, "宁夏"),
        (21, "青海"),
        (22, "山东"),
        (23, "山西"),
        (24, "陕西"),
        (25, "上海"),
        (26, "四川"),
        (27, "台湾"),
        (28, "天津"),
        (29, "西藏"),
        (30, "新疆"),
        (31, "云南"),
        (32, "浙江"),
        (33, "香港"),
        (34, "澳门"),
    }
    province = models.SmallIntegerField(verbose_name="省份", choices=province_choices)

    departmentNumber = models.IntegerField(verbose_name="科室数量", default=0)

    def __str__(self):
        return self.name


class department(models.Model):
    # 科室信息
    name = models.CharField(verbose_name="科室名称", max_length=32)
    drogsNumber = models.IntegerField(verbose_name="药物数量", default=0)
    devicesNumber = models.IntegerField(verbose_name="医疗设备数量", default=0)
    patientNumber = models.IntegerField(verbose_name="科室患者数量", default=0)
    # 外键约束
    #  - to, 与哪张表关联
    #  - to_field, 表中的哪一列关联
    #
    # django自动加上_id --> hospital_id(数据库之中的列)
    #
    # 删除医院，级联删除
    hospital = models.ForeignKey(verbose_name="所属医院", to="hospital", to_field="id", on_delete=models.CASCADE)

    #
    # 删除医院，hospital_id 置空
    # hospital = models.ForeignKey(to="hospital", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class drogs(models.Model):
    # 医药信息
    name = models.CharField(verbose_name="药品名称", max_length=32)
    # 外键关联科室
    department = models.ForeignKey(verbose_name="所属科室", to="department", to_field="id", on_delete=models.CASCADE)


class devicecs(models.Model):
    # 医疗设备信息
    name = models.CharField(verbose_name="医疗设备名称", max_length=32)
    # 外键关联科室
    department = models.ForeignKey(verbose_name="所属科室", to="department", to_field="id", on_delete=models.CASCADE)


class patient(models.Model):
    # 患者信息
    name = models.CharField(verbose_name="姓名", max_length=32)
    birthday = models.DateField(verbose_name="生日")

    # django的做的约束
    gender_choices = {
        (1, "男"),
        (2, "女"),
    }
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    age = models.IntegerField(verbose_name="年龄")
    # 外键关联医院
    hospital = models.ForeignKey(verbose_name="所属医院", to="hospital", to_field="id", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class patient_history(models.Model):
    # 患者病史记录
    dexcribe = models.CharField(verbose_name="病例描述", max_length=64)
    department = models.ForeignKey(verbose_name="所属科室", to="department", to_field="id", on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name="所属患者", to="patient", to_field="id", on_delete=models.CASCADE)


class insurance_company(models.Model):
    # 保险公司信息
    name = models.CharField(verbose_name="公司名称", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    insuranceProvideNumber = models.IntegerField(verbose_name="提供保险数量", default=0)

    def __str__(self):
        return self.name


class insurance_provide(models.Model):
    # 保险信息
    name = models.CharField(verbose_name="名称", max_length=32)
    amount = models.IntegerField(verbose_name="金额")
    insurance_company = models.ForeignKey(verbose_name="所属公司", to="insurance_company", to_field="id",
                                          on_delete=models.CASCADE)


class drogs_company(models.Model):
    # 医药公司信息
    name = models.CharField(verbose_name="公司名称", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    drogsProvideNumber = models.IntegerField(verbose_name="提供药品数量", default=0)
    drogsQuality = models.IntegerField(verbose_name="药品质量", default=0)

    def __str__(self):
        return self.name


class drogs_provide(models.Model):
    # 医药信息
    name = models.CharField(verbose_name="名称", max_length=32)
    amount = models.IntegerField(verbose_name="金额")
    drogs_company = models.ForeignKey(verbose_name="所属公司", to="drogs_company", to_field="id", on_delete=models.CASCADE)


class devices_company(models.Model):
    # 医药设备公司信息
    name = models.CharField(verbose_name="公司名称", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    devicesProvideNumber = models.IntegerField(verbose_name="提供设备数量", default=0)
    devicesQuality = models.IntegerField(verbose_name="设备质量", default=0)

    def __str__(self):
        return self.name


class devices_provide(models.Model):
    # 医疗公司信息
    name = models.CharField(verbose_name="名称", max_length=32)
    amount = models.IntegerField(verbose_name="金额")
    devices_company = models.ForeignKey(verbose_name="所属公司", to="devices_company", to_field="id",
                                        on_delete=models.CASCADE)


class insurance_evaluate(models.Model):
    # 保险公司评估结果列表
    insurance_name = models.CharField(verbose_name="保险公司名称", max_length=32)
    hospital_name = models.CharField(verbose_name="医院名称", max_length=32)
    score = models.IntegerField(verbose_name="评估分数")


class drogs_company_evaluate(models.Model):
    # 保险公司评估结果列表
    drogs_company_name = models.CharField(verbose_name="医药公司名称", max_length=32)
    hospital_name = models.CharField(verbose_name="医院名称", max_length=32)
    score = models.IntegerField(verbose_name="评估分数")


class devices_company_evaluate(models.Model):
    # 保险公司评估结果列表
    devices_company_name = models.CharField(verbose_name="医药公司名称", max_length=32)
    hospital_name = models.CharField(verbose_name="医院名称", max_length=32)
    score = models.IntegerField(verbose_name="评估分数")
