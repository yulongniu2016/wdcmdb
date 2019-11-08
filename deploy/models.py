#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

# Create your models here.
class TaskRecord(models.Model):
    tasktype = models.CharField(u"任务类型", max_length=50, null=False, blank=False)
    taskname = models.CharField(u"任务名称", max_length=50, null=False, blank=False)
    taskplaybook = models.TextField(u"内容", null=False, blank=False)
    taskuser = models.CharField(u"执行人", max_length=30, null=False, blank=False)
    tasktime = models.DateTimeField(u'开始时间', null=False, blank=False)
    taskstatus = models.CharField(u"结果", max_length=2, null=False, blank=False)
    tasktarget = models.TextField(u"执行详情", null=False, blank=False)
    taskendtime = models.DateTimeField(u'结束时间', null=True, blank=False)
    tasklog = models.CharField(u"任务日志", max_length=25, null=False, blank=False)
    
    
    def __str__(self):
        return self.tasktype
