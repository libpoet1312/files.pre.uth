# www/urls.py
from django.conf.urls import url
from www import views
from django.urls import path, include
from django.conf.urls.static import static

app_name = 'www'
urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.Info.as_view(), name='info'),
    #path('browse/', views.FileListView.as_view(), name='browse-files'),
    path('browse/', views.FileListView, name='browse-files'),
    path('file/<slug:the_slug>', views.FileDetailView.as_view(), name='file-detail'),
    path('profile/',views.get_user_profile, name='user_profile'),
    #path('files/', views.FileListView.as_view(), name='files'),
    path('file/create/', views.upload_file, name='create_file'),
    path('courses/', views.CourseListView.as_view(), name='browse-courses'),
    #path('courses/<slug:the_slug>', views.CourseDetail.as_view(), name='course-detail'),
    path('courses/<slug:the_slug>', views.FileListViewbyCourse.as_view(), name='course-detail'),
    path('search/', views.BootstrapFilterView, name='filter'),

]
