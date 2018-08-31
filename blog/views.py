from django.shortcuts import render,redirect,HttpResponse

from django.contrib import auth

from django.http import JsonResponse

from utils import ValidCode

from django.contrib.auth.decorators import login_required
# Create your views here.

from blog.Myforms import UserForm
from blog.models import UserInfo

def login(request):
    """
    登录：图形验证码
    :param request:
    :return:
    """
    
    # render(request,'blog/login.html')
    if request.method == 'POST':
        response = {"user":None,"msg":None}
        
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        
        # print("来自前端输入的验证码：",valid_code)

        valid_code_str = request.session.get("valid_code_str")
        # print("session里的验证码：",valid_code_str)
        
        if valid_code.upper() == valid_code_str.upper():
            """
            所以验证码不区分大小写
            """
            user_obj = auth.authenticate(username=user, password=pwd)
        
            if user_obj:
                auth.login(request,user_obj) # request.user == 当前登录对象
                response['user'] = user_obj.username
            else:
                response["msg"] = "用户名或密码错误"
                
            return JsonResponse(response)
        
        else:
            response['msg'] = '验证码错误'
            
        return JsonResponse(response)
        
    return render(request,'blog/login.html')


def register(request):
    """
    注册视图函数:
       get请求响应注册页面
       post(Ajax)请求,校验字段,响应字典
    :param request:
    :return:
    """

    if request.is_ajax():
        print(request.POST)
        form = UserForm(request.POST)
    
        response = {"user": None, "msg": None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
        
            # 生成一条用户纪录
            user = form.cleaned_data.get("user")
            print("user", user)
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
        
            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
        
            UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra)
    
        else:
            print(form.cleaned_data)
            print(form.errors)
            response["msg"] = form.errors
    
        return JsonResponse(response)
    
    form = UserForm()
    
    return render(request, "blog/register.html",{"form":form})




@login_required
def index(request):
    
    return render(request,"blog/index.html")


def logout(request):
    """
    注销视图
    :param request:
    :return:
    """
    auth.logout(request)  # request.session.flush()

    return redirect("/login/")

def agreement(request):
    
    return render(request,"blog/agreement.html")


def get_valid_code_img(request):
    """
    基于PIL模块动态生成响应状态码图片
    :param request:
    :return:
    """
    img_data = ValidCode.get_valid_code_img(request)

    return HttpResponse(img_data)