# Generated by Django 3.1.2 on 2021-04-01 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0012_cmdbbase_eip_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmdbbase',
            name='start_time',
            field=models.CharField(default='0000-00-00 00:00:00', max_length=100, verbose_name='实例创建时间'),
        ),
    ]
