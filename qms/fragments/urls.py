from django.urls import path 
from . import views 


urlpatterns = [ 
    path('', views.log, name='loginpage'),
    path('logout/', views.log_out, name='logout'),
    path('info/', views.list_all, name='listAll'),
    path('show/', views.show, name='show'),
    path('session/', views.sessions, name='session'),
    path('sessionD/', views.session_data, name='sessionD'),
    path('undo/<int:id>/', views.undo_session, name='undo'),
    path('undosess/<int:id>/', views.undo_session_confim, name='undosess'),
    path('update/<int:id>/', views.updateData, name='update'),
 
] 