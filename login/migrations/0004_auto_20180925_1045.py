# Generated by Django 2.1.1 on 2018-09-25 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_user_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('female', '女'), ('male', '男')], default='男', max_length=32),
        ),
    ]
