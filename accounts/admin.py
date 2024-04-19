from django.contrib import admin
from accounts.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'name', 'age', 'user_image', 'phoneNum', 'academicYear', 'created']

admin.site.register(User, UserAdmin)