from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('apply/', views.ProjectApplicationView.as_view(), name='project_apply'),
    path('apply/success/', views.ProjectApplicationSuccessView.as_view(), name='project_apply_success'),
]
