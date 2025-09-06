from django.contrib import admin
from stats.models import Developer, Repository
# Register your models here.

@admin.register(Repository)
class RepoAdmin(admin.ModelAdmin):
    list_display = ['name', 'developer']
@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'location', 'company',
                   'website_url', 'total_followers', 'total_following']
    search_fields = ['username', 'name']
