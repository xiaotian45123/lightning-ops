# Generated by Django 3.1.2 on 2021-03-24 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0009_auto_20210317_0112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cmdbbase',
            old_name='os_platform',
            new_name='os_system',
        ),
    ]