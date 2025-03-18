"""dbmsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import  settings
from pms.views import (
    login_view,
    register_view,
    dashboard_view,
    createnewteammember_view,
    teamembers_view,
    delete_item,
    edit_item,
    show_item,
    createproject_view,
    search_team_members,
    projectteams_view,
    delete_project,
    edit_project,
    show_project,
    createtask_view,
    task_view,
    delete_task_view,
    edit_task_view,
    logout_view,
    tasks_data_view,
    categories_data_view,
    designations_view_data,
    projects_data_view,
    project_categories_view,
    members_data_view,
    about_us_view,
    project_detail,
    review_detail,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login_view,name="login"),
    path('register/',register_view,name="register"),
    path('dashbord/',dashboard_view,name="home"),
    path('createnewteammember/',createnewteammember_view,name='createnewteammember'),
    path('teammembers/',teamembers_view,name='teammembers'),
    path('delete_item/<int:item_id>/',delete_item,name="delete_item"),
    path('edit_item/<int:item_id>/',edit_item,name="edit_item"),
    path('show_item/<int:item_id>/',show_item,name="show_item"),
    path('createproject/',createproject_view,name='createproject'),
    path('search_team_members/', search_team_members, name='search_team_members'),
    path('projectteams/',projectteams_view,name='projectteams'),
    path('delete_project/<int:item_id>/',delete_project,name="delete_project"),
    path('edit_project/<int:item_id>/',edit_project,name="edit_project"),
    path('show_project/<int:item_id>/',show_project,name="show_project"),
    path('createtask/',createtask_view,name="createtask"),
    path('tasks/',task_view,name='tasks'),
    path('delete_task/<int:item_id>',delete_task_view,name='delete_task'),
    path('edit_task/<int:item_id>',edit_task_view,name='edit_task'),
    path('logout/', logout_view, name='logout'),
    path('task_data/',tasks_data_view,name='task_data'),
    path('categories_data/',categories_data_view,name='categories_data'),
    path('designations_data/',designations_view_data,name='designations_data'),
    path('project_data/',projects_data_view,name='project_data'),
    path('project_categories/',project_categories_view,name='project_categories'),
    path('members_data/',members_data_view,name='members_data'),
    path('',about_us_view,name='about_us'),
    path('projects/<int:project_id>/',project_detail, name='project_detail'),
    path('projects/<int:project_id>/reviews/<int:review_id>/',review_detail, name='review_detail'),
]



urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
