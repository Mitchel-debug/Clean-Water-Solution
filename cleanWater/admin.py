from django.contrib import admin
from .models import Articles, User
# Register your models here.
admin.site.register(User)

class articleAdmin(admin.ModelAdmin):
    list_display = ('title', 'briefDesc','date')
    search_fields = ['title', 'content']
    prepopulated_fields = {'briefDesc': ('title',)}
admin.site.register(Articles, articleAdmin)
