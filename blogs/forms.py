#！/usr/bin/env.python
#coding:utf-8

from django.forms import ModelForm
from blogs import models

class BlogsForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'

        return ModelForm.__new__(cls)


    class Meta:
        from django.forms import widgets as wid
        model = models.Blogs
        fields = "__all__"
        exclude = ['user']

