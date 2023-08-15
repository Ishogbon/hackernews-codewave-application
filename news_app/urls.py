from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:page>/', views.homepage, name='homepage'),
    
    path('stories/', views.stories),
    path('stories/<int:page>/', views.stories),
    
    path('jobs/', views.jobs),
    path('jobs/<int:page>/', views.jobs),
    
    path('polls/', views.polls),
    path('polls/<int:page>/', views.polls),
    
    path('<str:item_source>/<str:item_type>/<int:item_id>/', views.item_page)
]