from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
'''
>
    > PageAdmin creates the display, -------------------------
    > we load it in with register ---------------------------
>
'''
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    #prepopulated_fields = {'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)