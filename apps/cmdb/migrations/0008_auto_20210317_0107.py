# Generated by Django 3.1.2 on 2021-03-17 01:07

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0007_auto_20210317_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmdbbase',
            name='extra_private_ip',
            field=models.JSONField(blank=True, default=base.models.JSONMulFieldDefault, null=True, verbose_name='扩展私有IP'),
        ),
        migrations.AddField(
            model_name='cmdbbase',
            name='extra_public_ip',
            field=models.JSONField(blank=True, default=base.models.JSONMulFieldDefault, null=True, verbose_name='扩展公网IP'),
        ),
    ]
