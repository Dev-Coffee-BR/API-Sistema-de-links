from django.contrib import admin
from core.models import Category, Link, FileType, File, CategoryLink, CategoryFile

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_in")
    list_display_links = ("id", "name", "created_in")
    list_per_page = 30


class LinkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", "created_in")
    list_display_links = ("id", "name", "url", "created_in")
    list_per_page = 30


class FileTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_in")
    list_display_links = ("id", "name", "created_in")
    list_per_page = 30


class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_in")
    list_display_links = ("id", "name", "description", "created_in")
    list_per_page = 30


class CategoryLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "link", "created_in")
    list_display_links = ("id", "category", "link", "created_in")
    list_per_page = 30


class CategoryFileAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "file", "created_in")
    list_display_links = ("id", "category", "file", "created_in")
    list_per_page = 30


admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(FileType, FileTypeAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(CategoryLink, CategoryLinkAdmin)
admin.site.register(CategoryFile, CategoryFileAdmin)
