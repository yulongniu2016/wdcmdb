#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from django.shortcuts import render
from django.http import HttpResponse
import os
from config.views import get_dir
from django.contrib.auth.decorators import login_required
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles
#from assets.models import Asset, HostGroup
#from assets.models import NIC
from assets.models import Server, VirtualMachine, HostGroup, IpInterface
from accounts.permission import permission_verify
from deploy.models import TaskRecord
import datetime
import json

# var info
ansible_dir = get_dir("a_path")
roles_dir = get_dir("r_path")
playbook_dir = get_dir("p_path")
script_dir = get_dir("a_s_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("deploy.log", level, log_path)
print("---> ansible_dir: ",ansible_dir)
print("---> roles_dir: ",roles_dir)
print("---> playbook_dir: ",playbook_dir)
print("---> script_dir: ",script_dir)
print("---> level: ",level)

# 这是在判断变量不为空的时候，需要根据获取到的变量在对应的roles下创建vars/main.yml文件，并把变量写进去文件中
def write_role_vars(roles, vargs):

    r_vars = vargs.split('\r\n')
    for r in roles:

        if vargs:
            if os.path.exists(roles_dir+r+"/vars"):
                pass
            else:
                os.mkdir(roles_dir+r+"/vars")

            with open(roles_dir+r+'/vars/main.yml', 'w+') as role_file:
                role_file.writelines("---\n")
                for x in r_vars:
                    rs = x + '\n'
                    role_file.writelines(rs)
    return True


@login_required()
@permission_verify()
def index(request):
    all_host = []
    servers = Server.objects.all()
    virtualmachines = VirtualMachine.objects.all()
    for server in servers:
        obj = Server.objects.get(id=server.id)
        all_host.append(server)
    for virtualmachine in virtualmachines:
        obj = VirtualMachine.objects.get(id=virtualmachine.id)
        all_host.append(virtualmachine)

    all_group = HostGroup.objects.all()
    all_dir = get_roles(roles_dir)
    all_pbook = get_playbook(playbook_dir)
    return render(request, 'deploy/sysdeploy.html', locals())


@login_required()
@permission_verify()
def splaybook(request):
    
    # This 总体记录功能
    tasktype = 'deploy'
    taskuser = request.user.name
    tasktime = datetime.datetime.now()
    
    ret = []
    title = []
    record = {}
    # temp.yml是在页面选择roles时，就创建一个临时的playbook，仅做一次性执行，每次都会不一样
    if os.path.exists(ansible_dir + '/temp.yml'):
        os.remove(ansible_dir + '/temp.yml')
    else:
        pass
    if request.method == 'POST':
        schedule = request.POST.getlist('mschedule')
        host = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        pbook = request.POST.getlist('splaybook', [])
        roles = request.POST.getlist('mroles', [])
        role_vars = request.POST.get('mvars')
        runtime = request.POST.get('mruntime')
        print("--->host=",host)
        print("--->schedule",schedule)

        # This 如果用户在页面选择的是主机
        if host:
            # This 如果用户选择了角色，并为选择具体playbook
            if roles:
                # This 如果用户选择了角色，并且设定了变量
                if role_vars:
                    write_role_vars(roles, role_vars)
                for h in host:
                    logging.info("==========ansible tasks start==========")
                    logging.info("User:"+request.user.name)
                    logging.info("host:"+h)
                    # This 在/etc/ansible/下创建一个临时playbook，叫做temp.yml，并往这个临时文件中写入hosts，以及角色
                    with open(ansible_dir + '/temp.yml', 'w+') as f:
                        flist = ['- hosts: '+h+'\n', '  gather_facts: true\n', '  roles:\n']
                        for r in roles:
                            rs = '    - ' + r + '\n'
                            flist.append(rs)
                            logging.info("Role:"+r)
                        f.writelines(flist)
                    # This 执行刚刚创建的临时playbook，并将输出信息记录到date中，并返回到ret里面
                    cmd = "ansible-playbook"+" " + ansible_dir+'/temp.yml'
                    pcmd = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
                    data = pcmd.communicate()
                    ret.append(data)
                    for d in data:
                        logging.info(d)
                    logging.info("==========ansible tasks end============")
                    
                # This 局部记录功能
                taskinfo = '在服务器：{}  上执行Ansible的角色 ：{}'.format(host, roles)
                
            else:
                # Jason: It's playbook run log
                # prunlog = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".log"
                hostsname = 'hosts_single'
                groupname = '[tms]'
                cmdcopy = "/bin/cp " + ansible_dir + "hosts " + ansible_dir + hostsname
                pcmdcopy = Popen(cmdcopy, stdout=PIPE, stderr=PIPE, shell=True)

                datacopy = pcmdcopy.communicate()
                print("--->datacopy: ", datacopy)
                filehost = open(ansible_dir + hostsname, 'a+')
                filehost.writelines(groupname+ '\n')
                #filehost.close()
                title.append('任务:')
                title.append(schedule[0])
                title.append('目标:')
                for h in host:
                    print("--->h: ",h)

                    title.append(h)
                    #hlist=[h]
                    # Jason: I will write hosts IP to host filel ansible_dir
                    filehost.writelines(h+'\n')
                filehost.close()
                print("--->title: ",title)

                for p in pbook:
                        for t in title:
                            ret.append(t)
                        ret.append('内容:')
                        ret.append(p)
                        # Jason: 禁用改写 .yml 文件
                        '''
                        # 
                        f = open(playbook_dir + p, 'r+')
                        flist = f.readlines()
                        flist[0] = '- hosts: '+h+'\n'
                        f = open(playbook_dir + p, 'w+')
                        f.writelines(flist)
                        f.close()
                        '''
                        cmd = "ansible-playbook"+" " + playbook_dir + p
                        print("--->cmd: ",cmd)
                        # Jason: It's a test
                        #f1 = open(playbook_dir + 'a.sh', 'w+')
                        #f1.writelines(cmd)
                        #f1.close()
                        # Jason: It's playbook run log
                        prunlog = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + ".log"
                        cmdshell = "/bin/sh " + script_dir + "playbook_run_single.sh " + hostsname + " " + p + " " + runtime + " " + prunlog
                        #cmdshell = "/bin/sh " + script_dir + "a.sh " + p + " " + runtime + " " + logname
                        print("--->cmdshell: ",cmdshell)
                        #pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                        pcmd = Popen(cmdshell, stdout=PIPE, stderr=PIPE, shell=True)
                        print("--->pcmd: ",pcmd)
                        data = pcmd.communicate()
                        print("--->data: ",data)
                        print("--->data: ", str(data[1],encoding="utf-8").split()[1])
                        #ret.append(data)

                        ret.append(str(data[1],encoding="utf-8").split()[1])
                        ret.append(str(data[1],encoding="utf-8").split('at')[1])
                        ret.append(prunlog)
                        print("--->ret: ", ret)
                        #logging.info("==========ansible tasks start==========")
                        logging.info("==========ansible tasks start==========")
                        logging.info("User:"+request.user.name)
                        logging.info("host:"+h)
                        logging.info("Playbook:"+p)
                        for d in data:
                            logging.info(d)
                        logging.info("==========ansible tasks end============")
                        
                        # This 局部记录功能
                        #taskinfo = '在服务器： {}  上执行： {}'.format(host, pbook)
                        #print("--->taskinfo: ",taskinfo)

                        status = pcmd.returncode
                        if status == 0:
                            taskstatus = 1
                        else:
                            taskstatus = 0
                        TaskRecord.objects.create(tasktype=tasktype, taskname=schedule[0],taskplaybook=pbook,taskuser=taskuser, tasktime=tasktime+datetime.timedelta(minutes=int(runtime)),
                                          taskstatus=taskstatus, tasktarget=host, tasklog=prunlog)
                        print("--->status: ", status)

        if group:
            if roles:
                if role_vars:
                    write_role_vars(roles, role_vars)
                for g in group:
                    logging.info("==========ansible tasks start==========")
                    logging.info("User:"+request.user.name)
                    logging.info("group:"+g)
                    f = open(ansible_dir + '/temp.yml', 'w+')
                    flist = ['- hosts: '+g+'\n', '  gather_facts: true\n', '  roles:\n']
                    for r in roles:
                        rs = '    - ' + r + '\n'
                        flist.append(rs)
                        logging.info("Role:"+r)
                    f.writelines(flist)
                    f.close()
                    cmd = "ansible-playbook"+" " + ansible_dir+'/temp.yml'
                    pcmd = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
                    data = pcmd.communicate()
                    ret.append(data)
                    for d in data:
                        logging.info(d)
                    logging.info("==========ansible tasks end============")
                    
                # This 局部记录功能
                taskinfo = '在服务器组：{}  上执行Ansible的角色 ：{}'.format(group, roles)

                    
            else:
                for g in group:
                    for p in pbook:
                        ret.append('===============[ Play is:'+p+' ]==============='+'\n')
                        ret.append('===============[ Objects is:'+g+' ]==============='+'\n')
                        f = open(playbook_dir + p, 'r+')
                        flist = f.readlines()
                        flist[0] = '- hosts: '+g+'\n'
                        f = open(playbook_dir + p, 'w+')
                        f.writelines(flist)
                        f.close()
                        cmd = "ansible-playbook"+" " + playbook_dir + p
                        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                        data = pcmd.communicate()
                        ret.append(data)
                        logging.info("==========ansible tasks start==========")
                        logging.info("User:"+request.user.name)
                        logging.info("Group:"+g)
                        logging.info("Playbook:"+p)
                        for d in data:
                            logging.info(d)
                        logging.info("==========ansible tasks end============")
                        
                # This 局部记录功能
                taskinfo = '在服务器组：{}  上执行Ansible的剧本 ：{}'.format(group, pbook)
                


        return render(request, 'deploy/result.html', locals())



# Record Update API
#@login_required()
#@permission_verify()
def srecordapi(request):
    
    # This 总体记录功能
    # shell usage: curl -d "taskid=20190402150833403980.log&status=2&endtime=2019-4-12" http://192.168.99.172:8000/deploy/srecordapi/
    if request.method == 'POST':
        print("---> It's POST")

        # It's get for json
        print("---> It's JSON")
        print("--->request.body: ", request.body)
        receive_data = json.loads(request.body.decode('utf-8'))
        print("--->receive_data ", receive_data)
        taskid = receive_data['tid']
        taskstatus = receive_data['status']
        taskendtime = receive_data['etime']
        print("--->tid, status, etime: ", receive_data['tid'],receive_data['status'],receive_data['etime'])
        '''
        # It's post
        taskid = request.POST.get('tid')
        taskstatus = request.POST.get('status')
        taskendtime = request.POST.get('etime')
        print("--->method: POST")
        print("--->tid: ", taskid)
        print("--->taskstatus: ",taskstatus)
        print("--->taskendtime: ",taskendtime)
        '''
    # Jason disab
    # http usage: http://192.168.99.172:8000/deploy/srecordapi/?taskid=20190402150833403980.log&status=1&endtime=2019-4-12
    if request.method == 'GET':
        print("---> It's GET")
        taskid = request.GET.get('tid')
        taskstatus = request.GET.get('status')
        taskendtime = request.GET.get('etime')

        print("--->taskstatus: ",taskstatus)
        print("--->taskendtime: ",taskendtime)




    if TaskRecord.objects.get(tasklog=taskid).taskstatus != '2':
        print("---> update, taskstatus: ",TaskRecord.objects.get(tasklog=taskid).taskstatus)
        trd = TaskRecord.objects.filter(tasklog=taskid).update(taskstatus=taskstatus, taskendtime=taskendtime)
        print("--->trd",trd)
    else:
        print("---> no update, taskstatus: ",TaskRecord.objects.get(tasklog=taskid).taskstatus)
    return HttpResponse(200)
    #return render(request, 'deploy/result.html', locals())


# This 这个功能是将组以及主机都查询出来，然后按照一定的格式，将查询出来的组以及主机写入ansible的hosts文件中
#@login_required()
#@permission_verify()
def host_sync(request):
    group = HostGroup.objects.all()
    ansible_file = open(ansible_dir+"/hosts", "w")
    servers = Server.objects.all()
    virtualmachines = VirtualMachine.objects.all()

    all_host = []
    for server in servers:
        #print("--->server: ",type(server))
        obj = Server.objects.get(id=server.id)
        all_host.append(server)
    for virtualmachine in virtualmachines:
        obj = VirtualMachine.objects.get(id=virtualmachine.id)
        all_host.append(virtualmachine)
    #print("--->all_host: ",type(all_host))

    for host in all_host:
        # This 因为资产表是有多个表通过外键关联的，ip信息在网卡表中，但是并非所有的网卡都会有IP地址，所以这里就先粗略获取到第一个IP地址
        #print("--->host.name",type(host))
        if 'Server' in str(type(host)):
            print("--->Server: ",str(type(host)))
            nicinfo = IpInterface.objects.filter(server_id = host.id)
        else:
           print("--->VirtualMachine: ",str(type(host)))
           nicinfo = IpInterface.objects.filter(virtualMachine_id = host.id)
        for i in nicinfo:
            if i.ipaddr is None:
                pass
            else:
                ip = i.ipaddr
        host_item = host.name+" "+"ansible_host="+ip+" "+"host_name="+host.name+"\n"
        ansible_file.write(host_item)
    for g in group:
        group_name = "["+g.name+"]"+"\n"
        ansible_file.write(group_name)
        get_member = HostGroup.objects.get(name=g.name)
        members_server = get_member.servers.all()
        members_virtualmachine = get_member.virtualmachine.all()
        # s表结构适配，serverlist是整理后的资产列表
        serverlist = []
        for server in members_server:
            obj = Server.objects.get(id=server.id)
            serverlist.append(server)
        for virtualmachine in members_virtualmachine:
            obj = VirtualMachine.objects.get(id=virtualmachine.id)
            serverlist.append(virtualmachine)
        for m in serverlist:
            group_item = m.name+"\n"
            ansible_file.write(group_item)
    ansible_file.close()
    logging.info("==========ansible tasks start==========")
    logging.info("User:"+request.user.name)
    logging.info("Task: sync cmdb info to ansible hosts")
    logging.info("==========ansible tasks end============")
    return HttpResponse("ok")
