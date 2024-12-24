from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="content"),
    path('add',views.add,name="add"),
    path('edit/<int:id>',views.content_edit,name="content-edit"),
    path('delete/<int:id>',views.content_delete,name="content-delete")
]
