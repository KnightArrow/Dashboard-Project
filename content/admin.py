from django.contrib import admin
from .models import Content,Category

class ContentAdmin(admin.ModelAdmin):
    list_display = ('owner','amount','description','category', 'date')
    search_fields = ['owner__username', 'description', 'category']  #Which field to use for search. #user field__nameinthefield for Foreign key
    list_filter = ('category', 'date')        #Have filter on right side.
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
        'fields': ('category',)
    }),
)



admin.site.register(Content,ContentAdmin)
admin.site.register(Category)
