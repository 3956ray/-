# Generated by Django 4.0.4 on 2022-05-02 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0009_alter_hospital_province_alter_patient_gender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drogs_provide',
            name='devices_company',
        ),
        migrations.AddField(
            model_name='drogs_provide',
            name='drogs_company',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='myproject.drogs_company', verbose_name='所属公司'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hospital',
            name='province',
            field=models.SmallIntegerField(choices=[(20, '宁夏'), (16, '江苏'), (19, '内蒙古'), (25, '上海'), (32, '浙江'), (23, '山西'), (14, '湖南'), (17, '江西'), (33, '香港'), (30, '新疆'), (29, '西藏'), (6, '广东'), (15, '吉林'), (22, '山东'), (3, '重庆'), (5, '甘肃'), (21, '青海'), (13, '湖北'), (31, '云南'), (27, '台湾'), (2, '北京'), (10, '河北'), (4, '福建'), (18, '辽宁'), (12, '黑龙江'), (7, '广西'), (24, '陕西'), (1, '安徽'), (11, '河南'), (9, '海南'), (34, '澳门'), (28, '天津'), (8, '贵州'), (26, '四川')], verbose_name='省份'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.SmallIntegerField(choices=[(2, '女'), (1, '男')], verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='userType',
            field=models.SmallIntegerField(choices=[(3, '医药供应商'), (1, '医院'), (2, '保险公司'), (4, '医疗设备供应商'), (5, '管理员')], max_length=32, verbose_name='用户种类'),
        ),
        migrations.CreateModel(
            name='devices_provide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('amount', models.IntegerField(verbose_name='金额')),
                ('devices_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myproject.devices_company', verbose_name='所属公司')),
            ],
        ),
    ]