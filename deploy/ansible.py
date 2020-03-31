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

from dwebsocket.decorators import accept_websocket, require_websocket
import paramiko


# var info
ansible_dir = get_dir("a_path")
ansible_data_dir = get_dir("a_d_path")
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
command = ''

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
    return render(request, 'deploy/ansible.html', locals())


#@login_required()
#@permission_verify()
def playbook(request):
    
    # This 总体记录功能
    tasktype = 'ansible-playbook'
    taskuser = request.user.name
    tasktime = datetime.datetime.now()
    
    # ret = []
    title = []
    # record = {}
    # temp.yml是在页面选择roles时，就创建一个临时的playbook，仅做一次性执行，每次都会不一样
    if os.path.exists(ansible_data_dir + '/site.yml'):
        os.remove(ansible_data_dir + '/site.yml')
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

        title.append('sch')
        title.append(schedule[0])
        title.append('obj')

        # 如果用户在页面选择的是主机
        if host:
            print("--->It's selected host")

            # It's alert window
            for h in host:
                print("--->h: ", h)
                title.append(h)
            print("--->title: ", title)

            # This 如果用户选择了roles，并为选择具体playbook
            if roles:
                print("--->It's selected Roles of host")
                title.append('act')
                title.append(roles)

                if role_vars:
                    write_role_vars(roles, role_vars)

                # This 在/etc/ansible/下创建一个临时playbook，叫做site.yml，并往这个临时文件中写入hosts，以及角色
                flist = ''
                with open(ansible_data_dir + 'site.yml', 'w+') as f:
                    for r in roles:
                        flist = flist + '- hosts: ' + str(host) + '\n' + '  gather_facts: false\n' + '  roles:\n' + '    - ' + r + '\n'
                    #print("--->flist:", flist)
                    f.writelines(flist)
                    # This 执行刚刚创建的临时playbook，并将输出信息记录到date中，并返回到ret里面
                    cmd = "ansible-playbook" + " " + ansible_data_dir + 'site.yml' + " -e ansible_ssh_pass='wandatms'"
                
            else:
                print("--->It's selected Playbook")
                title.append('act')
                title.append(pbook)

                print("--->pbook: ", pbook)
                pb = ''
                for p in pbook:
                    f = open(playbook_dir + p, 'r+')
                    flist = f.readlines()
                    # flist[0] = '- hosts: ' + str(title[3:]) + '\n'
                    flist[0] = '- hosts: ' + str(host) + '\n'
                    f = open(playbook_dir + p, 'w+')
                    f.writelines(flist)
                    f.close()
                    pb = pb + playbook_dir + p + ' '
                cmd = "ansible-playbook" + " " + pb + " -e ansible_ssh_pass='wandatms'"
                print("--->cmd: ",cmd)

        if group:
            print("--->It's selected group")
            for g in group:
                print("--->g: ", g)
                title.append(g)
            print("--->title: ", title)

            # This 如果用户选择了roles ，并为选择具体playbook
            if roles:
                print("--->It's selected Roles")
                title.append('act')
                title.append(roles)

                if role_vars:
                    write_role_vars(roles, role_vars)

                # This 在/etc/ansible/下创建一个临时playbook，叫做site.yml，并往这个临时文件中写入hosts，以及角色
                flist = ''
                with open(ansible_data_dir + 'site.yml', 'w+') as f:
                    for r in roles:
                        flist = flist + '- hosts: ' + str( group) + '\n' + '  gather_facts: false\n' + '  roles:\n' + '    - ' + r + '\n'
                    # print("--->flist:", flist)
                    f.writelines(flist)
                    # This 执行刚刚创建的临时playbook，并将输出信息记录到date中，并返回到ret里面
                    cmd = "ansible-playbook" + " " + ansible_data_dir + 'site.yml' + " -e ansible_ssh_pass='wandatms'"

            else:
                print("--->It's selected Playbook")
                title.append('act')
                title.append(pbook)

                print("--->pbook: ", pbook)
                pb = ''
                for p in pbook:
                    f = open(playbook_dir + p, 'r+')
                    flist = f.readlines()
                    flist[0] = '- hosts: ' + str(group) + '\n'
                    f = open(playbook_dir + p, 'w+')
                    f.writelines(flist)
                    f.close()
                    pb = pb + playbook_dir + p + ' '
                cmd = "ansible-playbook" + " " + pb + " -e ansible_ssh_pass='wandatms'"
                print("--->cmd: ", cmd)


    if request.method == "POST":
            #username = request.POST.get('username')
            #password = request.POST.get('password')
            serverinfo = {
                'schedule': title[title.index('sch')+1:2],
                'object': str(title[title.index('obj')+1:title.index('act')]),
                'act': title[title.index('act')+1:],
                'command': cmd
            }

    results = {
            'serverinfo': serverinfo,
        }
    print("--->results: ",results)

    #return render(request, 'deploy/ansibleresult.html', locals())
    return render(request, 'deploy/webshell.html', locals())


def exec_command(comm):
    hostname = '192.168.99.172'
    username = 'root'
    password = 'wsbfdl'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(comm)
    result = stdout.read()
    ssh.close()
    return result

@accept_websocket
def web_socket(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'ansible.html')
    else:
        for message in request.websocket:
            print("--->message1: ", message)
            message = message.decode('utf-8')
            print("--->message2: ", message)
            request.websocket.send(exec_command(message))
            ''''
            if message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                #command = 'sh /opt/b.sh'
                #command = 'ls -al /srv'
                #command = "ansible TMS  -e ansible_ssh_pass='wandatms' -m shell -a 'initctl status cqs'"
                #command = "ansible tms -i /etc/ansible/tms_hosts -e ansible_ssh_pass='wandatms' -m shell -a 'mke2fs -V'"
                command = "ansible tms -i /etc/ansible/tms_hosts -e ansible_ssh_pass='wandatms' -m shell -a 'curl -V'"
                #command = "ansible-playbook -i /etc/ansible/tms_hosts /var/lib/wdcmdb/data/ansible/playbook/mke2fs.yml -e ansible_ssh_pass='wandatms'"
                #command = "ansible-playbook -i /etc/ansible/test_hosts /var/lib/wdcmdb/data/ansible/playbook/mke2fs.yml -e ansible_ssh_pass='wandatms'"
                request.websocket.send(exec_command(command))  # 发送消息到客户端
            
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))
            '''



# Record Update API
#@login_required()
#@permission_verify()
def srecordapi(request):
    
    # This 总体记录功能
    if request.method == 'POST':
        print("---> It's POST")

        # It's get for json
        # http://10.199.89.212:7000/redisset/?name=xxx&value=xxx
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
        # shell usage: curl -H "Content-Type: application/json" -X POST -d '{"name":"neimeng","value":"huhehaote"}' http://10.199.89.212:7000/redisset/
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
