from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse
from ApiManager.models import ProjectInfo,ModuleInfo,ApiInfo,ApiHead,ApiParameter,ApiResponse,ApiParameterRaw
import requests
import json
from .forms import AddProjectForm,AddModuleForm
from django.http.response import HttpResponseRedirect
from ApiManager.TestEngine import getDb

# Create your views here.
def index(request):
    return render(request,"index.html")

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
        Response=CaseMessage.getApiResponse()
        results['info']=info
        results['headers']=headers
        results['Parameter']=Parameter
        results['ParameterRaw']=ParameterRaw
        results['Response']=Response
        results['context']='Empty'
        print(results)
        return render(request,'add_testcase.html',{'results':results})
    else:
        results['info']={}
        results['headers']={}
        results['Parameter']={}
        results['ParameterRaw']={}
        results['Response']={}
        results['context']='NoEmpty'
        return render(request,'add_testcase.html',{'results':results})

def del_testcase(request):
    ret={'status':True}
    try:
        nid=request.GET.get('value')
        ApiInfo.objects.filter(id=nid).delete()
    except Exception as e:
        ret['status']=False
    return HttpResponse(json.dumps(ret))
            
        
    
            
    