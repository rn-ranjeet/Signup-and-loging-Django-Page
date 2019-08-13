from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.PROTECT)

    #users website
    portfolio_site = models.URLField(blank=True)

    #profile Pictures
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    #method for printing this
    def __str__(self):
        return self.user.username
        #where username is default attribute of User
