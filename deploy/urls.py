#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from deploy import views, sysdeploy, deployrecord, ansible


urlpatterns = [

    # ansible功能模块开始
    url(r'ansible/$', ansible.index, name='ansible'),
    #url(r'^ansible/command/$', ansible.ansible_command, name='acommand'),
    url(r'^playbook/$', ansible.playbook, name='playbook'),
    url(r'ansible/web_socket/$', ansible.web_socket),

    url(r'sysdeploy/$', sysdeploy.index, name='sysdeploy'),
    url(r'^sysplaybook/$', sysdeploy.splaybook, name='sysplaybook'),
    url(r'^srecordapi/$', sysdeploy.srecordapi, name='srecordapi'),
    #
    url(r'^deployrecord/list/srecordapi/$', sysdeploy.srecordapi, name='srecordapi'),
    # sync hosts
    url(r'^host/sync/$', sysdeploy.host_sync, name='host_sync'),
    # This ansible功能模块结束

    
    # This 任务编排操作记录模块开始
    url(r'^deployrecord/list/$', deployrecord.drecord_list, name='drecord_list'),
    url(r'^deployrecord/list/drecord_export/$', deployrecord.drecord_export, name='drecord_export'),
    # This 任务编排操作记录模块结束
]
