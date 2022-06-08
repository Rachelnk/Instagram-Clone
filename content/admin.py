from django.contrib import admin
from .models import Post, Profile

# Register your models here.
admin.site.register(Post)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','created')
    search_fields = []
    readonly_fields=('created', 'updated')

admin.site.register(Profile, ProfileAdmin)
