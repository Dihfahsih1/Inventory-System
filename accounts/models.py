from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

# Create your models here.

class UserProfileManager(models.Manager):
    pass

class UserProfile(models.Model):
    ROLES = (
        ('', ''),
        ('Executive', 'Executive'),
        ('Manager', 'Manager'),
        ('Receptionist', 'Receptionist'),
        ('Accountant', 'Accountant'),
        ('Operations', 'Operations'),
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, default='', max_length=20)
    phone = models.IntegerField(default='+256701345376')
    hired_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)



    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs ['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        user_profile.save()

post_save.connect(create_profile, sender=User)