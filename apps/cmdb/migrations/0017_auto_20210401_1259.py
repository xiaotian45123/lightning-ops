# Generated by Django 3.1.2 on 2021-04-01 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0016_auto_20210401_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmdbbase',
            name='eip_ip',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='弹性IP地址'),
        ),
    ]
