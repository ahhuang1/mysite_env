# Generated by Django 2.1.1 on 2018-09-25 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20180925_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='login.User', verbose_name='创建微博的用户'),
        ),
    ]