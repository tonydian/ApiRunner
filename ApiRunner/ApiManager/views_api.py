'''
Created on 2018年7月13日

@author: Administrator
'''
import json
from ApiManager.models import ProjectInfo,ModuleInfo,ApiInfo
from ApiManager.forms import AddApiInfoForm
from django.http import HttpResponse

def get_project(request):
    project_list=[]
    try:
        results=ProjectInfo.objects.filter()
    except Exception as e:
        return HttpResponse(json.dumps({'status':10022,'message':e.reason}))
    else:
        if results:
            for result in results:
                project={}
                project['project_name']=result.project_name
                project['responsible_name']=result.responsible_name
                project['test_user']=result.test_user
                project['dev_user']=result.dev_user
                project['publish_app']=result.publish_app
                project['simple_desc']=result.simple_desc
                project['other_desc']=result.other_desc
                project_list.append(project)
        return HttpResponse(json.dumps({'status':200,'message':'success','value':project_list}))
    
def get_module(request):
    module_list=[]
    project_name=request.POST.get('project_name')
    if project_name=="请选择":
        return HttpResponse(json.dumps({'status':10022,'message':"no results"}))
    try:
        id=ProjectInfo.objects.filter(project_name=project_name)[0].id
        results=ModuleInfo.objects.filter(belong_project_id=id)
    except Exception as e:
        return HttpResponse(json.dumps({'status':10022,'message':"no results"}))
    else:
        if results:
            for result in results:
                module={}
                module['module_name']=result.module_name
                module['test_user']=result.test_user
                module['simple_desc']=result.simple_desc
                module['other_desc']=result.other_desc
                module_list.append(module)
        return HttpResponse(json.dumps({'status':200,'message':'success','value':module_list}))
    
def Save_ApiInfo(request):
    if request.method =='POST':
        form=AddApiInfoForm(request.POST)
        if form.is_valid():
            belong_project = form.cleaned_data['belong_project']
            belong_module = form.cleaned_data['belong_module']
            apiname = form.cleaned_data['apiname']
            httpType = form.cleaned_data['httpType']
            requestType = form.cleaned_data['requestType']
            apiAddress = form.cleaned_data['apiAddress']
            requestParameterType = form.cleaned_data['requestParameterType']
            project_id=ProjectInfo.objects.filter(project_name=belong_project).values('id')[0]['id']
            module_id=ModuleInfo.objects.filter(module_name=belong_module).values('id')[0]['id']
            if requestParameterType=="option1":
                requestParameterTypeName="form-data"
            else:
                requestParameterTypeName="raw"
            ApiInfo.objects.create(name=apiname,httpType=httpType,requestType=requestType,apiAddress=apiAddress,requestParameterType=requestParameterTypeName,belong_project_id=project_id,belong_module_id=module_id)
            
    else:
        form=AddApiInfoForm()
    return HttpResponse(json.dumps({'status':200,'message':'success','id':1}))
                
    
    
    