from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name="content"),
    path('add',views.add,name="add"),
    path('edit/<int:id>',views.content_edit,name="content-edit"),
    path('delete/<int:id>',views.content_delete,name="content-delete"),
    path('search-content',csrf_exempt(views.search_content),name="content-search")
]
