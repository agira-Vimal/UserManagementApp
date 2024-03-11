from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField 
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname=models.CharField(max_length=255,blank=True,null=True)
    phone_number=PhoneNumberField(null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
#create a USerProfile Instance automatically when user is registered
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile=UserProfile(user=instance)
        user_profile.save()
  
# Automate the save process       
post_save.connect(create_profile,sender=User)