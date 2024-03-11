from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User

admin.site.register(UserProfile)


#Mix User Raw data and Profile Data
class UserProfileInline(admin.StackedInline):
    model=UserProfile
    
#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model=User
    fields=['username','email']
    inlines=[UserProfileInline]
    
#Unregister the Old Way and Register the new way of getting Input in admin panel
admin.site.unregister(User)

admin.site.register(User,UserAdmin)