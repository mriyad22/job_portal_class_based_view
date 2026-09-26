from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'display_name', 'email', 'password')

admin.site.register(UserModel, UserAdmin)
admin.site.register([
    RecruiterProfileModel,
    SeekerProfileModel,
    JobPostModel,
    ApplyJobModel,
    CategoryModel
])
