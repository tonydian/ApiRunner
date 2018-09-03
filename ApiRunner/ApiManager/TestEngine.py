'''
Created on 2018年7月16日

@author: Administrator
'''
import requests
import unittest
from ApiManager.models import ApiHead
class getDb():
    def getApiHeader(self,belong_api_id):
        results=ApiHead.objects.filter(belong_api_id=belong_api_id)
        for item in results:
            print(item)
def RunTestCase(httpType,requestType,apiAddress,requestParameterType,header,Parameter):
    url=httpType+'://'+apiAddress
    if requestType=='get':
        r=requests.get(url,params=Parameter,headers=headers)
        print(r.text)
        print(r.json()['url'])

data = {
    'name': 'germey',
    'age': 22
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}    
RunTestCase("http", "get", "httpbin.org/get", "form-data",headers, data)
        
    