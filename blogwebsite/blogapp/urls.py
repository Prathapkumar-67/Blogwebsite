from django.urls import path
from . import views

urlpatterns = [
    # ...existing url patterns...
    path('aboutus/', views.aboutus, name='aboutus'),
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/edit/<int:blog_id>/', views.blog_edit, name='blog_edit'),
    path('blog/delete/<int:blog_id>/', views.blog_delete, name='blog_delete'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    # Add more URL patterns as needed
]
