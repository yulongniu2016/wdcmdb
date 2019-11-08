#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from assets import views

urlpatterns = [
    # 该url包括了客户端执行提交数据的url，也就是接口，后面带？参数的也是匹配这条utl规则
    # 服务器
    url(r'^server_list/$', views.server_list, name="server_list"),
    url(r'^server_list/(\d+)/$', views.server_detail, name="server_detail"),
    url(r'^asset_event_logs/(\d+)/$', views.asset_event_logs, name="asset_event_logs"),
    # 主机
    #url(r'^host_list/$', views.host_list, name="host_list"),
    #url(r'^host_list/(\d+)/$', views.host_detail, name="host_detail"),
    # 组管理
    url(r'^group/$', views.group, name='group'),
    url(r'^group/add/$', views.group_add, name='group_add'),
    url(r'^group/edit/(?P<group_id>\d+)/$', views.group_edit, name='group_edit'),
    url(r'^group/del/$', views.group_del, name='group_del'),
    url(r'^group/server_list/(?P<group_id>\d+)/$', views.groupserver_list, name='group_server_list'),
]
