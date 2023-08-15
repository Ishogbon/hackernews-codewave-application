from django.urls import path, re_path
from . import views
from . import api_views

urlpatterns = [
    path('type/', views.fetch_items_by_type),
    path('type/<str:item_type>/', views.fetch_items_by_type),
    
    path('source/', views.fetch_items_by_source),
    path('source/<str:item_source>/', views.fetch_items_by_source),
    
    path('item/<str:item_source>/<str:item_type>/<int:item_id>/', views.retrieve_item),
    
    path('store_item/', views.store_item),
    path('store_item', views.store_item),
    path('update_item', api_views.UpdateItemView.as_view()),
    path('update_item/', api_views.UpdateItemView.as_view()),
    
    re_path(r'^.*$', views.no_api)
]