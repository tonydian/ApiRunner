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

class RunApi():
    def __init__(self,projectId):
        self.projectId=projectId
        
    def RunProjectTask(self):
        project_name=get_object_or_404(ProjectInfo,id=self.projectId).project_name
        ApiDict=getApiByProject(self.projectId)
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
    for Task in TaskList:
        pass