from django.contrib import admin
from .models import Content1,Source

@admin.register(Content1)
class Content1Admin(admin.ModelAdmin):
    list_display = ('owner','amount','description','source', 'date')
    search_fields = ['owner__username', 'description', 'source']  #Which field to use for search. #user field__nameinthefield for Foreign key
    list_filter = ('source', 'date')        #Have filter on right side.
    ordering = ('-date',)                     #Ordering to be done according to which field.
    list_per_page = 1                         #Pagination.
    list_editable = ('amount',)               #Can be edited by viewing
    exclude = ('date',)                       #To exclude from editing page.
    readonly_fields = ('owner',)              #Field that should be read only.
    fieldsets = (                             #Display during edit page.
    (None, {
        'fields': ('owner', 'amount', 'description')
    }),
    ('More options', {
        'classes': ('collapse',),
        'fields': ('source',)
    }),
)
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass
