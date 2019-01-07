'''
Created on 2018年7月16日

@author: Administrator
'''
import requests
import json
import unittest
from ApiManager import  HTMLTestReportCN
from ApiManager.models import ApiInfo,ApiHead,ApiParameter,ApiResponse,ApiParameterRaw,ModuleInfo,ProjectInfo
class getDb():
    def __init__(self,api_id):
        self.api_id=api_id
        
    def getApiInfo(self):
        results=ApiInfo.objects.filter(id=self.api_id).select_related('belong_project','belong_module')
        info={}
        if results:
            for item in results:
                info['id']=item.id
                info['name']=item.name
                info['httpType']=item.httpType
                info['requestType']=item.requestType
                info['apiAddress']=item.apiAddress
                info['requestParameterType']=item.requestParameterType
                info['belong_project']=item.belong_project.project_name
                info['belong_module']=item.belong_module.module_name
            return info
        else:
            return {}
        
        
    def getApiHeader(self):
        results=ApiHead.objects.filter(belong_Api_id=self.api_id)
        headers={}
        if results:
            for item in results:
                headers[item.name]=item.value
            return headers
        else:
            return {}
        
    def getApiParameter(self):
        results=ApiParameter.objects.filter(belong_Api_id=self.api_id)
        Parameter={}
        if results:
            for item in results:
                Parameter[item.name]=item.value
            return Parameter
        else:
            return {}
        
    def getApiParemeter_all(self):
        results=ApiParameter.objects.filter(belong_Api_id=self.api_id)
        Parameter_all=[]
        Parameter={}
        if results:
            for item in results:
                Parameter['id']=item.id
                Parameter['name']=item.name
                Parameter['value']=item.value
                Parameter['type']=item.type
                if(item.required==False):
                    Parameter['required']='false'
                else:
                    Parameter['required']='true'
                Parameter['description']=item.description
                Parameter_all.append(Parameter)
                Parameter={}
            return Parameter_all
        else:
            return []     
   
    def getApiParameterRaw(self):
        results=ApiParameterRaw.objects.filter(belong_Api_id=self.api_id)
        ParameterRaw={}
        if results:
            for item in results:
                ParameterRaw['data']=item.data
            return ParameterRaw
        else:
            return {}
        
    def getApiResponse(self):
        results=ApiResponse.objects.filter(belong_Api_id=self.api_id)
        Response={}
        if results:
            for item in results:
                Response[item.name]=item.value
            return Response
        else:
            return {}
        
    def getApiResponse_all(self):
        results=ApiResponse.objects.filter(belong_Api_id=self.api_id)
        Response_all=[]
        Response={}
        if results:
            for item in results:
                Response['id']=item.id
                Response['name']=item.name
                Response['value']=item.value
                Response['type']=item.type
                if(item.required==False):
                    Response['required']='false'
                else:
                    Response['required']='true'
                Response['description']=item.description
                Response_all.append(Response)
                Response={}
            return Response_all
        else:
            return []
        
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
 
    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite  


def RunTestCase(api_id):
    DbData=getDb(api_id)
    info=DbData.getApiInfo()
    headers=DbData.getApiHeader()
    Parameter=DbData.getApiParameter()
    Response=DbData.getApiResponse()
    return run(info['httpType'],info['requestType'],info['apiAddress'],info['requestParameterType'],headers,Parameter,Response)
    
    
def run(httpType,requestType,apiAddress,requestParameterType,headers,Parameter,Response):
    url=httpType+'://'+apiAddress
    if requestType=='get':
        r=requests.get(url,params=Parameter,headers=headers)
        status={'result':'success'}
        for item,key in Response.items():
            if str(r.json()[item])!=key:
                status['result']='false'
                break
        response=r.json()
        response['result']=status['result']
        return json.dumps(response)
    if requestType=='post':
        r=requests.post(url,data=Parameter,headers=headers)
        print(r.text)
        status={'result':'success'}
        for item,key in Response.items():
            if str(r.json()[item])!=key:
                status['result']='false'
                break
        response=r.json()
        response['result']=status['result']
        return json.dumps(response)
    
def getApiByModule(module_id):
    id_list=[]
    ApiList=ApiInfo.objects.filter(belong_module_id=module_id)
    if ApiList.exists():
        for Api in ApiList:
            print(Api)
            id_list.append(Api.id)
    return id_list

def getApiByProject(Project_id):
    ModuleList=ModuleInfo.objects.filter(belong_project_id=Project_id)
    ApiDict={}
    for Module in ModuleList:
        Apis=[]
        ApiList=ApiInfo.objects.filter(belong_module_id=Module.id)
        for Api in ApiList:
            Apis.append(Api.id)
        ApiDict[Module.module_name]=Apis
    return ApiDict      
    
def getData(api_id):
    DbData=getDb(api_id)
    info=DbData.getApiInfo()
    headers=DbData.getApiHeader()
    Parameter=DbData.getApiParameter()
    Response=DbData.getApiResponse()
    data={}
    data['httpType']=info['httpType']
    data['requestType']=info['requestType']
    data['apiAddress']=info['apiAddress']
    data['requestParameterType']=info['requestParameterType']
    data['headers']=headers
    data['Parameter']=Parameter
    data['Response']=Response
    return data

class Testapi(ParametrizedTestCase):
    '''测试'''
    def test_case(self):
        url=self.param['httpType']+'://'+self.param['apiAddress']
        if self.param['requestType']=='get':
            r=requests.get(url,params=self.param['Parameter'],headers=self.param['headers'])
        if self.param['requestType']=='post':
            r=requests.post(url,data=self.param['Parameter'],headers=self.param['headers'])
        result=r.json()
        for item,key in self.param['Response'].items():
            self.assertEqual(str(result[item]), key)
            

            




        
    