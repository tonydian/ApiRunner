'''
Created on 2018年7月13日

@author: Administrator
'''
from django.urls import path
from ApiManager import views_api

urlpatterns = [
    path(r'get_project/', views_api.get_project, name='get_project'),
    path(r'get_module/', views_api.get_module, name='get_module'),
    path(r'Save_ApiInfo/',views_api.Save_ApiInfo,name='Save_ApiInfo'),
    path(r'Save_ApiHeader/',views_api.Save_ApiHeader,name='Save_ApiHeader'),
    path(r'Check_ApiName/',views_api.Check_ApiName,name='Check_ApiName'),
    path(r'Save_ApiParameter/',views_api.Save_ApiParameter,name='Save_ApiParameter'),
    path(r'Save_ApiResponse/',views_api.Save_ApiResponse,name='Save_ApiResponse'),
    path(r'run_testcase/',views_api.run_testcase,name='run_testcase'),
    path(r'Edit_ApiInfo/<int:eid>/',views_api.Edit_ApiInfo,name='Edit_ApiInfo'),
    path(r'get_quantity/',views_api.get_quantity,name='get_quantity'),
    path(r'run_testcase_unittest/',views_api.run_testcase_unittest,name='run_testcase_unittest'),
    path(r'show_report/<path:name>/',views_api.show_report,name='show_report'),
    path(r'run_test_module/',views_api.run_test_module,name='run_test_module')
    
]