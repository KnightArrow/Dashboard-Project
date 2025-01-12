from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name="content1"),
    path('add-content1',views.add,name="add-content1"),
    path('edit-content1/<int:id>',views.content1_edit,name="content1-edit"),
    path('delete-content1/<int:id>',views.content1_delete,name="content1-delete"),
    path('search-content1',csrf_exempt(views.search_content1),name="content1-search"),
    path("content1_summary_by_source",views.content1_summary_by_source,name="content1_summary_by_source"),
    path("stats",views.stas_view,name="content1stats"),
    path("export-csv",views.export_csv,name="export-csv-content1"),
    path("export-excel",views.export_excel,name="export-excel-content1"),
    path("export-pdf",views.export_pdf,name="export-pdf-content1"), 
]
