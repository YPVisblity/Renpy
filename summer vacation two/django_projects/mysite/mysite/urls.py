"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path,include
from pages import views as page_views

urlpatterns = [
    path('', page_views.home, name='home'),
    path('submit-solution/', page_views.submit_solution, name='submit_solution'),
    path(
        'accounts/login/',
        page_views.RoleLoginView.as_view(),
        name='login',
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ai-chat/', page_views.ai_chat, name='ai_chat'),
    path("polls/",include("polls.urls")),
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path("accounts/register/", page_views.register, name="register"),
    path("my-submissions/", page_views.my_submissions, name="submissions"),
    path("teacher/files/", page_views.teacher_files, name="teacher_files"),
    path("teacher/files/<path:filename>/", page_views.teacher_file_edit, name="teacher_file_edit"),
]
