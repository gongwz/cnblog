# _*_ encoding=utf-8 _*_

__author__ = 'weizhen'

from django import forms
from django.forms import widgets

from blog.models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError


class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           error_messages={"required":"请输入昵称"},
                           label = "昵 称",
                           widget=widgets.TextInput(attrs={"class": "form-control"}, ) # 自定义格式
                           )
    
    pwd = forms.CharField(max_length=32,
                          error_messages={"required": "密码不能为空"},
                          label="密 码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}, )  # 自定义格式
                          
                          )
    
    re_pwd = forms.CharField(max_length=32,
                             error_messages={"required": "请确认密码"},
                             label="确 认",
                             widget=widgets.PasswordInput(attrs={"class": "form-control"}, )  # 自定义格式

                             )
    
    email = forms.EmailField(max_length=32,
                             error_messages={"required": "请输入邮箱"},
                             label="邮  箱",
                             widget=widgets.EmailInput(attrs={"class": "form-control"}, )  # 自定义格式
                             )

    def clean_user(self):
        val = self.cleaned_data.get("user")
    
        user = UserInfo.objects.filter(username=val).first()
        if not user:
            return val
        else:
            raise ValidationError("该用户已注册!")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
    
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致!")
        else:
            return self.cleaned_data
