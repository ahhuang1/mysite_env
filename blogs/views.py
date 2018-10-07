from django.shortcuts import render,redirect,HttpResponse
from blogs import forms
from login import models
from blogs import models as Bmodels
# Create your views here.

def login_check(func):
    def check(request,*args,**kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/')
    return check

def login_admin(func):
    def check(request,*args,**kwargs):
        is_login = request.session.get('is_login')
        is_admin =request.session.get('user_permission')
        if is_login:
            if is_admin:
                return func(request,*args,**kwargs)
            else:
                return HttpResponse('非管理员用户无权操作')
        else:
            return redirect('/login/')
    return check

@login_admin
def blogs_add(request):
    if request.method == "POST":
        Blogsform = forms.BlogsForm(request.POST)
        if Blogsform.is_valid():
            if not request.session.get('user_permission',None):
                Blogsform.add_error('__all__','当前账号无管理员权限')
            else:
                form = Blogsform.save(commit=False)
                user_obj = models.User.objects.get(id=request.session["user_id"])
                form.user = user_obj
                form.save()
                return redirect('/blogs/')
    else:
        Blogsform = forms.BlogsForm()
    return render(request,'blogs/blogs_add.html',{"Blogsform":Blogsform,})

def blogs_list(request):
    obj = Bmodels.Blogs.objects.all()
    from blogs import utils
    page = int(request.GET.get('page', '1'))
    contacts = utils.fen_page(page, obj, 2)
    return render(request,"blogs/blogs_list.html",{"contacts":contacts,
                                                   })

@login_admin
def blogs_edit(request,blog_id):
    if request.method == "POST":
        obj = Bmodels.Blogs.objects.get(id=blog_id)
        Blogsform = forms.BlogsForm(request.POST,instance=obj)
        if Blogsform.is_valid():
            Blogsform.save()
    else:
        obj = Bmodels.Blogs.objects.get(id=blog_id)
        Blogsform = forms.BlogsForm(instance=obj)
    return render(request, 'blogs/blogs_edit.html', {"Blogsform": Blogsform, })

@login_admin
def blogs_delete(request):
    id = request.POST.get('id',None)
    if id:
        obj = Bmodels.Blogs.objects.get(id=id)
        obj.delete()
        return redirect('/blogs/manage/')

def blogs_index(request):
    obj = Bmodels.Blogs.objects.all()
    from blogs import utils
    page = int(request.GET.get('page','1'))
    contacts = utils.fen_page(page,obj,2)
    return render(request,"blogs/blogs_index.html",{"contacts":contacts})


def blogs_detail(request,detail_id):
    obj = Bmodels.Blogs.objects.get(id=detail_id)
    # BlogsForm = forms.BlogsForm(instance=obj)
    comment_list = Bmodels.Comment.objects.filter(blogs_id=detail_id).order_by('id')
    #递归实现评论树
    # comment_list = Node.create_tree(comment_list)

    #循环列表和字段引用生成评论树
    comment_list = Node.comment_dict(comment_list)
    return render(request,'blogs/blogs_detail.html',{'obj':obj,'comment_list':comment_list})

class Node:

    @staticmethod
    def digui(ret,row):
        for k in ret.keys():
            if row.parent.id == k:
                ret[k]['children'][row.id] = {
                    'content':row.content,
                    'user':row.user_id.name,
                    'id':row.id,
                    'children':  {},
                }
                return
            else:
                Node.digui(ret[k]['children'],row)

    @staticmethod
    def create_tree(comment_list):
        ret = {}
        for row in comment_list:
            if not row.parent:
                ret[row.id] = {
                    'content':row.content,
                    'user':row.user_id.name,
                    'id':row.id,
                    'children':  {},
                }
            else:
                #二级评论
                # for k in ret.keys():
                #     if row.parent == k:
                #         ret[k]['children'][row.id] = {
                #             'content': row.content,
                #             'user': row.user_id.name,
                #             'id': row.id,
                #             'children': {},
                #         }
                Node.digui(ret,row)

        return ret

    @staticmethod
    def comment_dict(comment_list):
        ret_end = []
        ret = []
        result = {}
        for r in comment_list:
            result[r.id] = {
                "content": r.content,
                "user": r.user_id.name,
                "id": r.id,
                "parent_id": r.parent.id if r.parent else None,
                "parent_name":r.parent.user_id.name if r.parent else None,
                "children": [],
            }
            ret.append(result[r.id])

        for row in ret:
            if not row['parent_id']:
                ret_end.append(row)
            else:
                if result.get(row['parent_id'],None):
                    result[row['parent_id']]['children'].append(row)
        return ret_end

@login_check
def blogs_comment(request,detail_id):
    obj_blogs = Bmodels.Blogs.objects.get(id=detail_id)
    user_id = request.session.get('user_id',None)
    obj_user = models.User.objects.get(id=user_id)
    parent_id = request.POST.get('parent_id',None)
    if parent_id:
        obj_comment = Bmodels.Comment.objects.get(id=parent_id)
    else:
        obj_comment = None
    content = request.POST.get('content')
    if not content:
        return HttpResponse('评论或者回复内容不能为空')
    obj = Bmodels.Comment.objects.create(blogs_id=obj_blogs,user_id=obj_user,parent=obj_comment,content=content)
    path = request.path.replace('/comment/','/')
    return redirect(path)

