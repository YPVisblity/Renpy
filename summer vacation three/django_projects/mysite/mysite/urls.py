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
from django.contrib.auth import views as auth_views


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

    path("accounts/password-reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="password_reset"),
    path("accounts/password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("accounts/password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("accounts/password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),

    path("api/posts/", page_views.get_posts, name="get_posts"),
    path("api/posts/create/", page_views.create_post, name="create_post"),
    path("api/posts/<int:post_id>/like/", page_views.toggle_like, name="toggle_like"),
    path("api/posts/<int:post_id>/reply/", page_views.create_reply, name="create_reply"),
]
