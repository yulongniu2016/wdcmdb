#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import django
from django import utils
import time, datetime
import re
#from assets.dashboard import AssetDashboard
from accounts.models import UserProfile
from accounts.models import LoginRecord
from assets.models import Rack, Cinema, Server, StorageSystem 
#from assets.models import EventLog
#from broken_record.models import BrokenRrecord
#from appconf.models import Product, Project
#from fast_excute.models import FastexcudeRecord

@login_required
def index(request):
    # This 登录记录相关 开始
    date_time = datetime.datetime.now()
    year_month = time.strftime('%Y-%m',time.localtime(time.time()))
    login_record = LoginRecord.objects.filter(logintime__contains=year_month)
    #login_record = LoginRecord.objects.filter()[:2]
    for e in login_record:
        print(e.logintime)
    usercount = UserProfile.objects.count()
    login_user = []
    for i in login_record:
        if i.name not in login_user:
            login_user.append(i.name)
    login_user_count = len(login_user)  
    user_activity = '{:.0f}'.format(login_user_count/usercount*100)
    # This 登录记录相关 结束

     # This 在线用户统计相关 开始
    # This获取没有过期的session
    sessions =Session.objects.filter(expire_date__gte=datetime.datetime.now())
    print('--->sessions:',sessions)
    uid_list = []
    # This 获取session中的userid
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    print('--->uid_list:',uid_list)
 
    # Thist 根据userid查询user
    online_user = UserProfile.objects.filter(id__in=uid_list)
    online_user_count = len(online_user)
    print('--->online_user:',online_user,online_user_count)
    # This 在线用户统计相关 结束

    # This 登录详细信息相关 开始
    # This 以logintime降序排列，前面加个横杠就是降序
    login_record_10 = LoginRecord.objects.order_by('-logintime')[:10]
    # This 登录详细信息相关 结束


    # 报表统计
    # rack count
    rackcount = Rack.objects.count()
    rack_on_count = Rack.objects.filter(status=1).count()
    if rack_on_count > 0:
       rack_on_rate = '{:.0f}'.format(rack_on_count/rackcount*100)
    else:
       rack_on_rate = 0

    # cinema count
    cinemacount = Cinema.objects.count()
    cinema_on_count = Cinema.objects.filter(cinema_status='openup').count()
    cinema_off_count = Cinema.objects.filter(cinema_status='closedown').count()
    if cinema_on_count > 0:
       cinema_on_rate = '{:.0f}'.format(cinema_on_count/cinemacount*100)
    else:
       cinema_on_rate = 0

    # server count
    servercount = Server.objects.count()
    server_production_count = Server.objects.filter(status='production').count()
    server_implementation_count = Server.objects.filter(status='implementation').count()
    server_obsolete_count = Server.objects.filter(status='obsolete').count()
    server_stock_count = Server.objects.filter(status='stock').count()

    # StorageSystem count
    storagesystemcount = StorageSystem.objects.count()
    storagesystem_production_count = StorageSystem.objects.filter(status='production').count()
    storagesystem_implementation_count = Server.objects.filter(status='implementation').count()
    storagesystem_obsolete_count = Server.objects.filter(status='obsolete').count()
    storagesystem_stock_count = Server.objects.filter(status='stock').count()

    # 临时数据
    business_impact_time_rate = 0
    even_change_count_rate = 0
    event_log_10 = 0
    results = {
        'usercount': usercount,
        'user_activity': user_activity,
        'online_user': online_user,
        'online_user_count': online_user_count,
        'login_record_10': login_record_10,
        'rackcount': rackcount,
        'cinemacount': cinemacount,  
        'servercount': servercount, 
        'storagesystemcount': storagesystemcount,
        #
        'business_impact_time_rate': business_impact_time_rate,
        'even_change_count_rate': even_change_count_rate,
        'event_log_10': event_log_10,
        'assetcount': '1000',
        'idc_count': '5',
        'product_count': '10',
        'project_count': '20',
    }
    return render(request,'index.html', results)
    #return render(request,'default.html', results)


# 登录验证模块
def acc_login(request):
    # 如果请求的方式为POST，则为提交账号密码的操作
    if request.method == "POST":
        vcode = request.POST.get('vcode')
        session_code = request.session['verifycode']
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        print("--->",username,password,user)
        # 判断用户的账号密码是否验证通过
        if user is not None:
            # 判断用户输入的验证码是否正确
            if vcode.upper() == session_code:
                # valid_end_time这个是账户的有效期结束时间
                if user.valid_end_time: #设置了end time
                    # 秋飞修改
                    #if django.utils.timezone.now() > user.valid_begin_time and django.utils.timezone.now()  < user.valid_end_time:
                    # 如果当前的时间大于账号的有效开始时间，并且当前时间小于用户的有效结束时间，就登录成功
                    if utils.timezone.now() > user.valid_begin_time and utils.timezone.now()  < user.valid_end_time:
                        auth.login(request,user)
                        # 这个很重要，是设置用户登录后session保存多久，这里设置了30分钟，30分钟后需要重新登录
                        request.session.set_expiry(60*300)
                        #print 'session expires at :',request.session.get_expiry_date()
                        # This 用户登录记录到数据库
                        user = request.user
                        ipaddr = request.META['REMOTE_ADDR']
                        LoginRecord.objects.create(loginsource=ipaddr, name=user)
                        # 验证通过，返回首页
                        return HttpResponseRedirect('/')
                    else:
                        # 如果验证没通过，则返回登录页后，提示过期信息
                        return render(request,'login.html',{'login_err': '您的账号已过期，请联系管理员！'})
                # 秋飞修改
                #elif django.utils.timezone.now() > user.valid_begin_time:
                # 如果没有设置过期结束时间，那么则会查看当前时间是否比账号生效开始时间大，如果大就可以登录
                elif utils.timezone.now() > user.valid_begin_time:
                        auth.login(request,user)
                        # 这个很重要，是设置用户登录后session保存多久，这里设置了30分钟，30分钟后需要重新登录
                        request.session.set_expiry(60*300)
                        # This 用户登录记录到数据库
                        user = request.user
                        ipaddr = request.META['REMOTE_ADDR']
                        LoginRecord.objects.create(loginsource=ipaddr, name=user)
                        return HttpResponseRedirect('/')
            else:
                return render(request,'login.html',{'login_err': '您输入的验证码错误，请重新输入！'})

        # 如果页面提交过来的账号密码没通过验证，则提示账号或者密码错误
        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    # 如果请求的方式不是post，那么直接返回login.html页面，也就是登录页
    else:
        return render(request, 'login.html')

# 账号退出模块    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

