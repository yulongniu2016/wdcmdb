#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from deploy.models import TaskRecord
from subprocess import Popen, PIPE

#@login_required()
#@permission_verify()
def drecord_list(request):
    all_records = TaskRecord.objects.all().order_by('-tasktime')
    results = {
        'all_records': all_records,
    }
    print("--->results: ",results)
    return render(request, 'deploy/drecords_list.html', results)


#@login_required()
#@permission_verify()
def drecord_export(request):
    ret = []
    if request.method == 'GET':
        print("---> log detail")
        tasklog = request.GET.get('tlog')
        taskname = request.GET.get('tname')


        print("--->tasklog: ", tasklog)
    for i in range(0,1):
      #cmdcopy = "tail -n10 /var/opt/itelftool/logs/ansible.log"
      cmdcopy = "tail -n10 /var/opt/itelftool/logs/" + tasklog
      pcmdcopy = Popen(cmdcopy, stdout=PIPE, stderr=PIPE, shell=True)
      output = pcmdcopy.communicate()
      print("--->output: ",type(output))
      print("--->output: ", output)

      ret.append(output[0])
      print("--->ret: ", ret)
      print("--->type: ",type(ret))
    return render(request, 'deploy/drecord_export.html', locals())

