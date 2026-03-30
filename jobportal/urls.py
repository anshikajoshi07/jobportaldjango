"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path ,include
from job.views import *
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('admin_cre/', admin_cre, name="admin_cre"),
    path('recurater/', recurater, name="recurater"),
    path('loginreq',loginreq,name="loginreq"),
    path('recu_home/',recu_home, name="recu_home"),
    path('about/', about, name="about"),
    path('user/', user, name="user"),
    path('loginuser/', loginuser, name="loginuser"),
    path('loginadmin/', loginadmin, name="loginadmin"),
    path('user_home/', user_home, name="user_home"),
    path('dashboard/',dashboard, name="dashboard"),
    path('jobs/edit/<int:job_id>/',edit_job, name="edit_job"),
    path('jobs/delete/<int:job_id>/',delete_job, name="delete_job"),
    path('admin_home/',admin_home, name="admin_home"),
    path('admin_nav/',admin_nav, name="admin_nav"),
    path('view_user/',view_user, name="view_user"),
    path('view_recu/',view_recu, name="view_recu"),
    path('job_list/',job_list, name="job_list"),
    path('delete_user/<int:pid>',delete_user, name="delete_user"),
    path('Change_status/<int:pid>',Change_status, name="Change_status"),
    path('candidat_app/',candidat_app,name="candidat_app"),
    path('change_passwordreq/',change_passwordreq, name="change_passwordreq"),
    path('nrreq/',nrreq, name="nrreq"),
    path('logout/',logout, name="logout"),
    path('job_listuser/',job_listuser, name="job_listuser"),
    path('change_passwordUser/',change_passwordUser, name="change_passwordUser"),
    # path('application_form/',application_form, name="application_form"),
    path('application_form/', application_form, name="application_form"),
]
# +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)