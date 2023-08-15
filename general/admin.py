from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','meta_key','meta_value')


admin.site.register(User)
admin.site.register(Announcement)