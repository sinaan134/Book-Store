from django.contrib import admin
from . models import Book,Cart

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['name','author','price','description']
    # list_filter = ['author','price']
    # list_editable = ['price']
    # search_fields = ['name','author']
    # list_per_page = 2

    actions = ['mark_free']

    def mark_free(self,request,queryset):
        queryset.update(price=0)
        self.message_user(request,"selected book is free")
    mark_free.short_description = 'mark selected book as free'



admin.site.register(Book,BookAdmin)
admin.site.register(Cart)