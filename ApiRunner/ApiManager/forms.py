#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年6月30日

@author: neildian
'''
from django import forms
 
class AddProjectForm(forms.Form):
    project_name = forms.CharField()
    responsible_name = forms.CharField()
    test_user = forms.CharField()
    dev_user = forms.CharField()
    publish_app = forms.CharField()
    simple_desc = forms.CharField()
    other_desc = forms.CharField()
    
class AddModuleForm(forms.Form):
    module_name = forms.CharField()
    belong_project=forms.CharField()
    test_user = forms.CharField()
    simple_desc = forms.CharField()
    other_desc = forms.CharField()
    
class AddApiInfoForm(forms.Form):
    belong_project=forms.CharField(required=False)
    belong_module=forms.CharField(required=False)
    apiname=forms.CharField(required=False)
    httpType=forms.CharField(required=False)
    requestType=forms.CharField(required=False)
    apiAddress=forms.CharField(required=False)
    requestParameterType=forms.CharField(required=False)
    description=forms.CharField(required=False)
    
class AddApiHead(forms.Form):
    api_id=forms.CharField()
    name=forms.CharField()
    value=forms.CharField()
    
class AddApiParameter(forms.Form):
    belong_Api = forms.CharField()
    name = forms.CharField()
    type = forms.CharField()
    value = forms.CharField()
    description = forms.CharField(required=False)

class AddApiParameter_raw(forms.Form):
    belong_Api = forms.CharField()
    data = forms.CharField()

class AddApiResponse(forms.Form):
    belong_Api = forms.CharField()
    name = forms.CharField()
    type = forms.CharField()
    value = forms.CharField()
    description = forms.CharField(required=False)
    
class AddTaskInfo(forms.Form):
    belong_project=forms.CharField()
    task_name=forms.CharField()
    task_type=forms.CharField()
    executeTime =forms.DateTimeField(required=False)
    fixedTime=forms.CharField(required=False)
 