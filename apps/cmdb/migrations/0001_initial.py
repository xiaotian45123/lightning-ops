# Generated by Django 3.1.2 on 2021-02-20 23:55

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CMDBBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='名称')),
                ('private_ip', models.GenericIPAddressField(db_index=True, unique=True, verbose_name='私有IP地址')),
                ('public_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='公网IP地址')),
                ('hostname', models.CharField(db_index=True, max_length=100, verbose_name='主机名')),
                ('mem_total', models.FloatField(verbose_name='内存(G)')),
                ('cpu_total', models.IntegerField(verbose_name='CPU(核)')),
                ('state', models.IntegerField(choices=[(1, 'running'), (2, 'stopped')], verbose_name='运行状态')),
                ('type', models.IntegerField(choices=[(1, 'idc'), (2, 'vm'), (3, 'cloud'), (4, 'container')], verbose_name='机器类型')),
                ('zone', models.CharField(blank=True, max_length=100, null=True, verbose_name='位置/可用区')),
                ('region', models.CharField(blank=True, max_length=100, null=True, verbose_name='机房/地域')),
                ('platform', models.IntegerField(choices=[(1, 'aws'), (2, 'ali'), (3, 'ten'), (4, 'hw'), (5, 'azure'), (0, '')], default=0, verbose_name='平台')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': 'CMDB基础表',
                'verbose_name_plural': 'CMDB基础表',
            },
        ),
        migrations.CreateModel(
            name='SSH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('user', models.CharField(max_length=32, verbose_name='ssh用户名')),
                ('password', models.CharField(max_length=32, verbose_name='ssh用户密码')),
                ('port', models.IntegerField(verbose_name='ssh端口')),
            ],
            options={
                'verbose_name': 'ssh表',
                'verbose_name_plural': 'ssh表',
            },
        ),
        migrations.CreateModel(
            name='JoinCMDBBaseTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('key', models.CharField(db_index=True, max_length=32, verbose_name='Key')),
                ('value', jsonfield.fields.JSONField(default={}, verbose_name='Value')),
                ('cmdb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.cmdbbase', verbose_name='CMDB基表')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tag',
            },
        ),
        migrations.AddField(
            model_name='cmdbbase',
            name='ssh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmdb.ssh', verbose_name='关联的ssh'),
        ),
    ]
