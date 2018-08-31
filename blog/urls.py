from django.urls import path,include,re_path

from blog import views

urlpatterns = [
    re_path(r'^get_valid_code_img/',views.get_valid_code_img),
    re_path(r'^agreement/',views.agreement)
]


