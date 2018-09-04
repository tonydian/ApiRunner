'''
Created on 2018年7月16日

@author: Administrator
'''
import requests
import unittest
from ApiManager.models import ApiInfo,ApiHead,ApiParameter,ApiResponse
class getDb():
    def __init__(self,api_id):
        self.api_id=api_id
        
    def getApiInfo(self):
        results=ApiInfo.objects.filter(id=self.api_id)
        info={}
        if results:
            for item in results:
                info['httpType']=item.httpType
                info['requestType']=item.requestType
                info['apiAddress']=item.apiAddress
                info['requestParameterType']=item.requestParameterType
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
        
    def getApiResponse(self):
        results=ApiResponse.objects.filter(belong_Api_id=self.api_id)
        Response={}
        if results:
            for item in results:
                Response[item.name]=item.value
            return Response
        else:
            return {}
        
        
        


def RunTestCase(api_id):
    DbData=getDb(api_id)
    info=DbData.getApiInfo()
    headers=DbData.getApiHeader()
    Parameter=DbData.getApiParameter()
    Response=DbData.getApiResponse()
    run(info['httpType'],info['requestType'],info['apiAddress'],info['requestParameterType'],headers,Parameter,Response)
    
    
    
    
def run(httpType,requestType,apiAddress,requestParameterType,headers,Parameter,Response):
    url=httpType+'://'+apiAddress
    if requestType=='get':
        r=requests.get(url,params=Parameter,headers=headers)
        for item,key in Response.items():
            print(str(r.json()[item]))
            print(key)
        
    