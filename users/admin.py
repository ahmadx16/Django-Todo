from django.contrib import admin

from .models import Profile, DateTime

class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'date_of_birth', 'bio']
    list_display = ['user', 'date_of_birth']
    list_filter = ['user']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(DateTime)
