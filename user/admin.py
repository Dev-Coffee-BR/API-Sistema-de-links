from django.contrib import admin
from user.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "email", "date_joined")
    list_display_links = ("id", "first_name", "email", "date_joined")
    list_per_page = 30


admin.site.register(User, UserAdmin)
