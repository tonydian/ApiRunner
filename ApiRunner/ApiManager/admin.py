from django.contrib import admin
from ApiManager.models import ProjectInfo,ModuleInfo,ApiInfo,ApiHead,ApiParameter,ApiParameterRaw,ApiResponse
# Register your models here.
admin.site.register(ProjectInfo)
admin.site.register(ModuleInfo)
admin.site.register(ApiInfo)
admin.site.register(ApiHead)
admin.site.register(ApiParameter)
admin.site.register(ApiParameterRaw)
admin.site.register(ApiResponse)