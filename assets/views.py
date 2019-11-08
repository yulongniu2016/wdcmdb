#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import json

#from assets import core, models, asset_handle, utils, admin
from assets import models, admin 
from assets import tables
#from assets.dashboard import  AssetDashboard
#from assets.forms import IdcForm, CabinetForm, GroupForm
from assets.forms import GroupForm
#from assets.models import IDC,Cabinet, HostGroup
from assets.models import HostGroup
#from accounts.permission import permission_verify

# 资产列表页，资产列表展示
#@login_required
#@permission_verify()
def server_list(request):
    print("--->server_list:")
    # 获取资产，tables的table_filter函数就是用来找出过滤条件，筛选出对应资产
    # <QuerySet [<Asset: <id:1 name:LinuxServer1>>, <Asset: <id:2 name:LinuxServer2>>, ... ,<Asset: <id:6 name:CqsServer002>>]>
    server_obj_list = tables.table_filter(request, admin.ServerAdmin, models.Server)
    print("--->asset_obj_list:", server_obj_list)    

    # 排序的结果 for server_obj_list
    order_res = tables.get_orderby(request, server_obj_list, admin.ServerAdmin)
    print("--->order_res_: ", order_res)

    # 翻页，list_per_page每页多少条数据
    paginator = Paginator(order_res[0], admin.ServerAdmin.list_per_page)
    # 从请求中获取到的页码，客户请求的是第几页
    page = request.GET.get('page')
    print("--->page:", page)
    try:
        asset_objs = paginator.page(page)
    except PageNotAnInteger:
        asset_objs = paginator.page(1)
    except EmptyPage:
        asset_objs = paginator.page(paginator.num_pages)
    print("--->asset_objs: ", asset_objs)
    print("--->models.Asset: ", models.Asset)
    print("--->admin.AssetAdmin: ", admin.ServerAdmin)
    #print("--->order_res: ", order_res)
    print("--->table_obj: start")
    # table_obj就是页面所需要展示的数据 -- models.Asset 中的资产信息
    table_obj = tables.TableHandler(request,
                                    models.Server,
                                    admin.ServerAdmin,
                                    asset_objs,
                                    order_res
                                    )

    # Jason 修改
    print("--->table_obj type: ",type(table_obj))
    print("--->table_obj: ",table_obj)
    print("--->:ginator ",paginator)

    return render(request, 'assets/server.html', {'table_obj': table_obj, 'paginator': paginator})
    #return render(request, 'assets/default.html')

#@login_required
#@permission_verify()
def server_detail(request, server_id):
    if request.method == "GET":
        try:
            server_obj = models.Server.objects.get(id=server_id)
            print('--->',server_obj)

        except ObjectDoesNotExist as e:
            return render(request, 'assets/server_detail.html', {'error': e})
        return render(request, 'assets/server_detail.html', {"asset_obj": server_obj})
   

#@login_required
#@permission_verify()
def asset_event_logs(request, asset_id):
    if request.method == "GET":
        log_list = asset_handle.fetch_asset_event_logs(asset_id)
        return HttpResponse(json.dumps(log_list, default=utils.json_datetime_handler))

# 虚拟机列表展示
#@login_required
#@permission_verify()
def virtualmachine_list(request):
    allvirtualmachine = VirtualMachine.all()
    context = {
        'allvirtualmachine': allvirtualmachine
    }
    return render(request, 'assets/virtualmachine.html', context)

#@login_required
#@permission_verify()
def group(request):
    allgroup = HostGroup.objects.all()
    context = {
        'allgroup': allgroup
    }
    return render(request, 'assets/group.html', context)


#@login_required
#@permission_verify()
def groupserver_list(request, group_id):
    grp = HostGroup.objects.get(id=group_id)
    print("--->grp: ", grp)
    servers = grp.servers.all()
    virtualmachines = grp.virtualmachine.all()
    print("--->servers: ", servers)
    serverlist = []
    for server in servers:
        #print("--->server: ", server)
        obj = models.Server.objects.get(id=server.id)
        for item in  models.IpInterface.objects.filter(server_id=server.id):
           ip = item.__dict__['ipaddr']
           id = item.__dict__['id']
           name = {'id': id, 'name': server}
           #print("--->name: ", name)
        serverlist.append(server)
    #print("--->grouplist:",server, obj, ip, serverlist)
    virtualmachinelist = []
    for virtualmachine in virtualmachines:
        obj = models.VirtualMachine.objects.get(id=virtualmachine.id)
        serverlist.append(virtualmachine)
      
    return render(request, 'assets/group_server_list.html', {'serverlist':serverlist})


#@login_required
#@permission_verify()
def group_add(request):
    if request.method == "POST":
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "assets/group_base.html", locals())
    else:
        display_control = "none"
        group_form = GroupForm()
        return render(request, "assets/group_base.html", locals())


#@login_required
#@permission_verify()
def group_edit(request, group_id):
    project = HostGroup.objects.get(id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('group'))
    else:
        form = GroupForm(instance=project)
    display_control = "none"
    results = {
        'group_form': form,
        'group_id': group_id,
        'request': request,
        'display_control': display_control,
    }
    return render(request, 'assets/group_base.html', results)


#@login_required
#@permission_verify()
def group_del(request):
    group_id = request.GET.get('id', '')
    if group_id:
        HostGroup.objects.filter(id=group_id).delete()
    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        if group_items:
            for n in group_items:
                HostGroup.objects.filter(id=n).delete()
    allgroup = HostGroup.objects.all()
    return render(request, "assets/group.html", locals())
