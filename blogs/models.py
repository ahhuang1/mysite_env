from django.db import models
from login import models as m
# Create your models here.

class Blogs(models.Model):
    user = models.ForeignKey(m.User,on_delete=models.CASCADE,verbose_name="创建微博的用户",null=True,blank=True)
    name = models.CharField(max_length=128,verbose_name="标题")
    summary = models.CharField(max_length=400,verbose_name="摘要")
    content = models.TextField(verbose_name="微博内容")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(max_length=64)
    user_id = models.ForeignKey(m.User,on_delete=models.CASCADE)
    blogs_id = models.ForeignKey('Blogs',on_delete=models.CASCADE)
    parent = models.ForeignKey("self",related_name="o",blank=True,null=True,on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)