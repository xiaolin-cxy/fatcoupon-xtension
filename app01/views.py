from django.shortcuts import render,redirect
from app01 import models
# Create your views here.

def depart_list(request):
    """部门列表"""
    #去数据库中获取所有的部门列表
    #[对象，对象，对象]
    querysite=models.Department.objects.all()


    return  render(request,'depart_list.html',{"querysite":querysite})

def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request,'depart_add.html')

    # 获取用户POST提交过来的数据(title输入为空)
    title=request.POST.get("title")

    #保存到数据库
    models.Department.objects.create(title=title)

    #重定向
    return redirect("/depart/list/")

def depart_delete(request):
    """删除部门"""
    #获取ID
    nid=request.GET.get('nid')
    #删除
    models.Department.objects.filter(id=nid).delete()

    #重定向
    return redirect("/depart/list/")

def depart_edit(request,nid):
    """修改部门"""
    #根据uid,获取它的数据[obj,]
    if request.method=="GET":
        row_object=models.Department.objects.filter(id=nid).first()
        # print(row_object.id,row_object.title)
        return render(request,"depart_edit.html", {"row_object": row_object})
    #获取用户提交的标配
    title=request.POST.get("title")
    #根据id找到数据库中的数据并进行更新
    models.Department.objects.filter(id=nid).update(title=title)

    #重定向
    return redirect("/depart/list/")

def user_list(request):
    """用户管理"""

    #获取所有用户列表
    queryset=models.UserInfo.objects.all()
    '''
    #python语法获取数据
        for obj in queryset:
        print(obj.id,obj.name,obj.account,obj.create_time.strftime("%Y-%m-%d"),obj.gender,obj.get_gender_display(),obj.depart.id,obj.depart.title)
        # print(obj.name,obj.depart_id) #获取数据库中存储的字段值
        # xx= models.Department.objects.filter(id=obj.depart_id).first()
        # xx.title
        # obj.depart_id     #获取数据库中存储的字段值
        # obj.depart.title  #根据id自动去关联的表中获取那一行数据的Depart对象
        # obj.gender #1/2
        # obj.get_gender_display() #get_字段名称_display()
    '''

    return render(request,"user_list.html",{"queryset":queryset})

def user_add(request):
    """添加用户"""
    if request.method=="GET":

        context={
         'gender_choice' :models.UserInfo.gender_choices,
         'depart_list':models.Department.objects.all()
        }
        return render(request,"user_add.html",context)
    #获取用户提交的数据
    user=request.POST.get("user")
    password=request.POST.get("password")
    age=request.POST.get("age")
    ac=request.POST.get("ac")
    ctime=request.POST.get("ctime")
    gender=request.POST.get("gender")
    dp=request.POST.get("dp")

    #添加到数据库
    models.UserInfo.objects.create(name=user,password=password,age=age,account=ac,
                                   create_time=ctime,gender=gender,
                                   depart_id=dp)

    #返回到用户列表页面
    return  redirect("/user/list/")


#modelForm
from django import  forms
class UserModelForm(forms.ModelForm):
    name =forms.CharField(min_length=3,label="用户名")
    class Meta:
        model=models.UserInfo
        fields=["name","password","age","account","create_time","gender","depart"]
        # widgets={
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password":forms.PasswordInput(attrs={"class":"form-control"})
        # }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #循环找到所有的插件，添加了class=”form-control“
        for name,field in self.fields.items():
            # if name=="password":
            #     continue
            field.widget.attrs={"class":"form-control","placeholder":field.label}

def user_model_form_add(request):
    """添加用户（modelform版本）"""
    if request.method  == "GET":
        form=UserModelForm()
        return  render(request,"user_model_form_add.html",{"form":form})
    #用户POST提交数据，数据校验。
    form=UserModelForm(data=request.POST)
    if form.is_valid():
        #数据合法，保存到数据库
        # print(form.cleaned_data)
        form.save()
        return  redirect("/user/list/")
    else:
        #校验失败,显示错误信息
        return  render(request,"user_model_form_add.html",{"form":form})


def user_edit(request,nid):
    """编辑用户"""
    row_object=models.UserInfo.objects.filter(id=nid).first()
    if request.method=="GET":
        # 根据ID去数据库获取要编辑的那一行数据(对象)
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form= UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        #默认保存的是用户输入的所有数据，如果想要在用户输入以外的值
        #form.instance.字段名=值
        form.save()
        return  redirect('/user/list')
    return  render(request,'user_edit.html',{"form":form})


def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return  redirect('/user/list/')
