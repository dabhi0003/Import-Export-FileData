from core.views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/",home,name="home"),
    path("register/",register,name="register"),
    path("",login1,name="login"),
    path("logout/",logout1,name="logout"),
    path("export/",export_to_csv,name="export"),
    path("import/",import_csv,name="import"),
]   
