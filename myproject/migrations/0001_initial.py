# Generated by Django 4.0.4 on 2022-04-24 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
    ]