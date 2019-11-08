"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app import views
from accounts import VerifyCode
from assets import urls as asset_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # name，简单来说，name 可以用于在 templates，models，views ..... 中得到对应的网址，相当于给网址取了个名字，只要这个名字不变，网址变了也能通过名字获取到。
    # 首页
    url(r'^$',views.index,name="index"),
    # 登录页
    url(r'^login/$',views.acc_login, name='login'),
    # 验证码功能
    url(r'^verifycode/$', VerifyCode.verifycode),
    # 退出页
    url(r'^logout/$', views.logout, name='logout'),

    # 用户管理url入口
    url(r'^accounts/', include('accounts.urls')),
    
    # 模块部分
    # 以asset开头的url均跳转到assets模块里的rest_urls,urls里
    url(r'^asset/', include(asset_urls)),

    # 系统批量部署url入口
    url(r'^deploy/', include('deploy.urls')),

]
