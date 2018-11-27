'''
Created on 2018年7月16日

@author: Administrator
'''
from ApiManager.models import TaskInfo,ProjectInfo,ApiInfo
from ApiManager.TestEngine import getApiByProject,Testapi,ParametrizedTestCase,getData
from django.shortcuts import render,get_object_or_404
import request
import unittest
import datetime
from django.conf import settings
from ApiManager.HTMLTestReportCN import HTMLTestRunner


def RunProjectTask(projectId):
    project_name=get_object_or_404(ProjectInfo,id=projectId).project_name
    ApiDict=getApiByProject(projectId)
    i=0
    suite=unittest.TestSuite()
    for key,value in ApiDict.items():
        if value: 
            NewClassName='Testapi'+str(i)
            NewClass=type(NewClassName,(Testapi,),{})
            NewClass.__name__=key
            for api in value:
                data=getData(api)
                NewClass.test_case.__doc__= get_object_or_404(ApiInfo,id=api).name
                suite.addTest(ParametrizedTestCase.parametrize(NewClass,param=data))
            i=i+1
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    filePath =settings.REPORT_DIRS+[nowTime]+['.html']
    fp = open(''.join(filePath),'wb+')
    runner =HTMLTestRunner(stream=fp,title='任务:'+project_name,tester="admin")
    runner.run(suite)
    fp.close()

def getTaskInfo():
    TaskList=TaskInfo.objects.filter()
    TaskResult={}
    for Task in TaskList:
        message=[]
        calendar={}
        message.append(Task.type)
        message.append(Task.belong_project_id)
        if Task.type=='once':
            executeTime=Task.executeTime
            calendar['year']=executeTime.year
            calendar['month']=executeTime.month
            calendar['day']=executeTime.day
            calendar['hour']=executeTime.hour
            calendar['minute']=executeTime.minute
            calendar['second']=executeTime.second
        if Task.type=='everyday':
            fixedTime=Task.fixedTime
            d=datetime.datetime.strptime(fixedTime, '%H:%M:%S')
            calendar['hour']=d.hour
            calendar['minute']=d.minute
            calendar['second']=d.second
        if Task.type=='Mon-fri':
            fixedTime=Task.fixedTime
            d=datetime.datetime.strptime(fixedTime, '%H:%M:%S')
            calendar['hour']=d.hour
            calendar['minute']=d.minute
            calendar['second']=d.second
        message.append(calendar)
        TaskResult[Task.id]=message
    return TaskResult
            
            
        