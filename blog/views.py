from django.shortcuts import render,redirect,HttpResponse

from django.contrib import auth

from django.http import JsonResponse

from utils import ValidCode

# Create your views here.


def login(request):
    
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


def index(request):
    
    return render(request,"blog/index.html")



def get_valid_code_img(request):
    """
    基于PIL模块动态生成响应状态码图片
    :param request:
    :return:
    """
    img_data = ValidCode.get_valid_code_img(request)

    return HttpResponse(img_data)