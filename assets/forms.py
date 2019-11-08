#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *
from .models import HostGroup

class GroupForm(forms.ModelForm):
    '''
    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        value = cleaned_data.get('name')
        try:
            Cabinet.objects.get(name=value)
            self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
        except Cabinet.DoesNotExist:
            pass
        return cleaned_data
    '''
    class Meta:
        model = HostGroup
        exclude = ("id", )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'desc': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:450px;'}),

        }


