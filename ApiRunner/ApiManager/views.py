from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse
from ApiManager.models import ProjectInfo,ModuleInfo,ApiInfo,ApiHead,ApiParameter,ApiResponse,ApiParameterRaw,TaskInfo,UserInfo
import requests
import json
from .forms import AddProjectForm,AddModuleForm,AddTaskInfo
from django.http.response import HttpResponseRedirect
from ApiManager.TestEngine import getDb
from django.conf import settings
import os
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    return render(request,"Login.html")

def login_action(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        request.session['user']=username
        response=HttpResponseRedirect('/index/')
        return response
    else:
        return render(request,'Login.html',{'error':'username or password error!'})

@login_required
def index(request):
    return render(request,"index.html")


def register_action(request):
    if request.method=='POST':
        password = request.POST.get('register_password', '')
        repeat_password = request.POST.get('repeat_register_password', '')
        email=request.POST.get('register_email', '')
        username = request.POST.get('register_username', '')
        if UserInfo.objects.filter(username=username):
            return render(request,'Login.html',{'register_error':'用户已经存在'})
        else:
            new_user = UserInfo.objects.create_user(username=username, password=password,email=email)
            new_user.save()
        return render(request,'Login.html',{'error':'注册成功'})
        
        
    




def api_get(request):
    url=request.POST.get('url','')
    try:
        r=requests.get(url)
    except Exception as e:
        r=None
    return render(request,"index.html",{'resp':r})


def project_list(request):
    project_list=ProjectInfo.objects.all()
    return render(request,'project_list.html',{'projects':project_list})

def add_project_page(request,eid=0):
    if eid !=0:
        project_name = get_object_or_404(ProjectInfo,id=eid).project_name
        responsible_name = get_object_or_404(ProjectInfo,id=eid).responsible_name
        test_user = get_object_or_404(ProjectInfo,id=eid).test_user
        dev_user = get_object_or_404(ProjectInfo,id=eid).dev_user
        publish_app = get_object_or_404(ProjectInfo,id=eid).publish_app
        simple_desc = get_object_or_404(ProjectInfo,id=eid).simple_desc
        other_desc = get_object_or_404(ProjectInfo,id=eid).other_desc
        return render(request,'add_project.html',{'project_name':project_name,'responsible_name':responsible_name,'test_user':test_user,'dev_user':dev_user,'publish_app':publish_app,'simple_desc':simple_desc,'other_desc':other_desc,'status':True,'project_id':eid})
    else:
        return render(request,'add_project.html')

def add_project(request):
    if request.method =='POST':
        form=AddProjectForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['project_name']
            responsible_name = form.cleaned_data['responsible_name']
            test_user = form.cleaned_data['test_user']
            dev_user = form.cleaned_data['dev_user']
            publish_app = form.cleaned_data['publish_app']
            simple_desc = form.cleaned_data['simple_desc']
            other_desc = form.cleaned_data['other_desc']
            ProjectInfo.objects.create(project_name=project_name,responsible_name=responsible_name,test_user=test_user,dev_user=dev_user,publish_app=publish_app,simple_desc=simple_desc,other_desc=other_desc)
    else:
        form=AddProjectForm()
    return HttpResponseRedirect('/project_list/')

def del_project(request):
    ret={'status':True}
    try:
        nid=request.GET.get('value')
        ProjectInfo.objects.filter(id=nid).delete()
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))

def edit_project(request):
    if request.method =='POST':
        form=AddProjectForm(request.POST)
        if form.is_valid():
            project_id=request.POST.get('project_id')
            project_name = form.cleaned_data['project_name']
            responsible_name = form.cleaned_data['responsible_name']
            test_user = form.cleaned_data['test_user']
            dev_user = form.cleaned_data['dev_user']
            publish_app = form.cleaned_data['publish_app']
            simple_desc = form.cleaned_data['simple_desc']
            other_desc = form.cleaned_data['other_desc']
            ProjectInfo.objects.filter(id=project_id).update(project_name=project_name,responsible_name=responsible_name,test_user=test_user,dev_user=dev_user,publish_app=publish_app,simple_desc=simple_desc,other_desc=other_desc)
    else:
        form=AddProjectForm()
    return HttpResponseRedirect('/project_list/')

def get_project(request):
    ret={'status':True}
    try:
        project_list_list=ProjectInfo.objects.all()
        ret['project_list']=project_list
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))

    
def module_list(request):
    module_list=ModuleInfo.objects.all().select_related('belong_project')
    return render(request,'module_list.html',{'modules':module_list})

def add_module_page(request,eid=0):
    project_list=ProjectInfo.objects.all()
    if eid !=0:
        module_name = get_object_or_404(ModuleInfo,id=eid).module_name
        belong_project = get_object_or_404(ModuleInfo,id=eid).belong_project
        test_user = get_object_or_404(ModuleInfo,id=eid).test_user
        simple_desc = get_object_or_404(ModuleInfo,id=eid).simple_desc
        other_desc = get_object_or_404(ModuleInfo,id=eid).other_desc
        return render(request,'add_module.html',{'module_name':module_name,'belong_project':belong_project,'test_user':test_user,'simple_desc':simple_desc,'other_desc':other_desc,'status':True,'module_id':eid,'projects':project_list})
    else:
        return render(request,'add_module.html',{'projects':project_list})

def add_module(request):
    if request.method =='POST':
        form=AddModuleForm(request.POST)
        if form.is_valid():
            module_name = form.cleaned_data['module_name']
            test_user = form.cleaned_data['test_user']
            simple_desc = form.cleaned_data['simple_desc']
            other_desc = form.cleaned_data['other_desc']
            belong_project_id=ProjectInfo.objects.filter(project_name=form.cleaned_data['belong_project']).values('id')
            ModuleInfo.objects.create(module_name=module_name,test_user=test_user,simple_desc=simple_desc,other_desc=other_desc,belong_project_id=belong_project_id[0]['id'])
    else:
        form=AddModuleForm()
    return HttpResponseRedirect('/module_list/')

def del_module(request):
    ret={'status':True}
    try:
        nid=request.GET.get('value')
        ModuleInfo.objects.filter(id=nid).delete()
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))

def edit_module(request):
    if request.method=="POST":
        form=AddModuleForm(request.POST)
        if form.is_valid():
            module_id=request.POST.get('module_id')
            module_name = form.cleaned_data['module_name']
            test_user = form.cleaned_data['test_user']
            simple_desc = form.cleaned_data['simple_desc']
            other_desc = form.cleaned_data['other_desc']
            belong_project_id=ProjectInfo.objects.filter(project_name=form.cleaned_data['belong_project']).values('id')
            ModuleInfo.objects.filter(id=module_id).update(module_name=module_name,test_user=test_user,simple_desc=simple_desc,other_desc=other_desc,belong_project_id=belong_project_id[0]['id'])
    else:
        form=AddModuleForm()
    return HttpResponseRedirect('/module_list/')

def testcase_list(request):
    testcase_list=ApiInfo.objects.all().select_related('belong_project','belong_module')
    return render(request,'testcase_list.html',{'testcase_list':testcase_list})


def add_testcase_page(request,eid=0):
    results={}
    if eid!=0:
        CaseMessage=getDb(eid)
        info=CaseMessage.getApiInfo()
        headers=CaseMessage.getApiHeader()
        Parameter=CaseMessage.getApiParemeter_all()
        ParameterRaw=CaseMessage.getApiParameterRaw()
        Response=CaseMessage.getApiResponse_all()
        results['info']=info
        results['headers']=headers
        results['Parameter']=Parameter
        results['ParameterRaw']=ParameterRaw
        results['Response']=Response
        results['context']='NoEmpty'
        print(results)
        return render(request,'add_testcase.html',{'results':results})
    else:
        results['info']={}
        results['headers']={}
        results['Parameter']={}
        results['ParameterRaw']={}
        results['Response']={}
        results['context']='Empty'
        return render(request,'add_testcase.html',{'results':results})

def del_testcase(request):
    ret={'status':True}
    try:
        nid=request.GET.get('value')
        ApiInfo.objects.filter(id=nid).delete()
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))

def report_list(request):
    filePath =settings.REPORT_DIRS
    fileList=[]
    for root,dirs,files in os.walk(''.join(filePath)):
        for file in files:
            fileList.append(file)       
    return render(request,'report_list.html',{'fileList':fileList})

def del_report(request):
    ret={'status':True}
    try:
        value=request.GET.get('value')
        filePath =settings.REPORT_DIRS+[value]
        os.remove(''.join(filePath))
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))

def add_task_page(request,eid=0):
    project_list=ProjectInfo.objects.all()
    if eid!=0:
        name=get_object_or_404(TaskInfo,id=eid).name
        type=get_object_or_404(TaskInfo,id=eid).type
        executeTime=get_object_or_404(TaskInfo,id=eid).executeTime
        belong_project=get_object_or_404(TaskInfo,id=eid).belong_project
        fixedTime=get_object_or_404(TaskInfo,id=eid).fixedTime
        return render(request,'add_task.html',{'task_id':eid,'task_name':name,'belong_project':belong_project,'type':type,'executeTime':executeTime,'fixedTime':fixedTime,'projects':project_list})
    else:
        return render(request,'add_task.html',{'task_name':"",'projects':project_list})


def add_task(request):
    if request.method=="POST":
        form=AddTaskInfo(request.POST)
        print(form)
        if form.is_valid():
            belong_project_id=ProjectInfo.objects.filter(project_name=form.cleaned_data['belong_project']).values('id')
            task_name = form.cleaned_data['task_name']
            type = form.cleaned_data['task_type']
            executeTime = form.cleaned_data['executeTime']
            fixedTime=form.cleaned_data['fixedTime']
            TaskInfo.objects.create(belong_project_id=belong_project_id[0]['id'],name=task_name,type=type,executeTime=executeTime,fixedTime=fixedTime)
    return HttpResponseRedirect('/task_list/')

def task_list(request):
    task_list=TaskInfo.objects.all().select_related('belong_project')
    return render(request,'task_list.html',{'tasks':task_list})

def edit_task(request):
    if request.method=="POST":
        form=AddTaskInfo(request.POST)
        print(form)
        if form.is_valid():
            task_id=request.POST.get('task_id')
            print(task_id)
            task_name = form.cleaned_data['task_name']
            type = form.cleaned_data['task_type']
            executeTime = form.cleaned_data['executeTime']
            fixedTime=form.cleaned_data['fixedTime']
            belong_project_id=ProjectInfo.objects.filter(project_name=form.cleaned_data['belong_project']).values('id')
            TaskInfo.objects.filter(id=task_id).update(belong_project_id=belong_project_id[0]['id'],name=task_name,type=type,executeTime=executeTime,fixedTime=fixedTime)
    else:
        form=AddModuleForm()
    return HttpResponseRedirect('/task_list/')

def del_task(request):
    ret={'status':True}
    try:
        nid=request.GET.get('value')
        TaskInfo.objects.filter(id=nid).delete()
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))
    
    
        
        
    
    
    
            
                
            
        
    
            
        
    
            
    