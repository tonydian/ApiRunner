"""ApiRunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from ApiManager import views as ApiManager_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',ApiManager_views.index),
    path('api_get/',ApiManager_views.api_get),
    path(r'api/',include('ApiManager.urls')),
#     项目管理路由
    path('project_list/',ApiManager_views.project_list),
    path('add_project/',ApiManager_views.add_project_page),
    path('add_project_action/',ApiManager_views.add_project),
    path('del_project/',ApiManager_views.del_project),
    path('edit_project/<int:eid>/',ApiManager_views.add_project_page),
    path('edit_project/',ApiManager_views.edit_project),
#     模块管理路由
    path('module_list/',ApiManager_views.module_list),
    path('add_module/',ApiManager_views.add_module_page),
    path('add_module_action/',ApiManager_views.add_module),
    path('del_module/',ApiManager_views.del_module),
    path('edit_module/<int:eid>/',ApiManager_views.add_module_page),
    path('edit_module/',ApiManager_views.edit_module),
    path('add_testcase/',ApiManager_views.add_testcase_page),
    path('testcase_list/',ApiManager_views.testcase_list),
    path('del_testcase/',ApiManager_views.del_testcase),
    path('edit_testcase/<int:eid>/',ApiManager_views.add_testcase_page),
    path('report_list/',ApiManager_views.report_list),
    path('del_report/',ApiManager_views.del_report),
    path('add_task/',ApiManager_views.add_task_page),
    path('add_task_action/',ApiManager_views.add_task),
    path('task_list/',ApiManager_views.task_list)
]

