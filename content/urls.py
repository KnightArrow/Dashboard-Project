from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name="content"),
    path('add',views.add,name="add"),
    path('edit/<int:id>',views.content_edit,name="content-edit"),
    path('delete/<int:id>',views.content_delete,name="content-delete"),
    path('search-content',csrf_exempt(views.search_content),name="content-search"),
    path("content_summary_by_category",views.content_summary_by_category,name="content_summary_by_category"),
    path("stats",views.stas_view,name="stats"),
    path("export-csv",views.export_csv,name="export-csv"),
    path("export-excel",views.export_excel,name="export-excel"),
    path("export-pdf",views.export_pdf,name="export-pdf"), 
]
