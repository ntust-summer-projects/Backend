from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as timezone
 
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        NORMAL = "NORMAL", 'Normal'
        COMPANY = "COMPANY", 'Company'
    
    role = models.CharField(max_length=50, choices=Role.choices,default = Role.ADMIN)
    
    def get_profile(self):
        return Profile.objects.all().filter(user=self.id)
 
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "ADMIN" or instance.role == 'Admin':
#         Profile.objects.bulk_create(
#             [Profile(user=instance,meta_key="name"),
#              Profile(user=instance,meta_key="phone"),
#              Profile(user=instance,meta_key="IsAdmin",meta_value="true")]
#             ) 
#     elif created and instance.role == "NORMAL" or instance.role == 'Normal':
#         Profile.objects.bulk_create(
#             [Profile(user=instance,meta_key="name"),
#              Profile(user=instance,meta_key="phone"),
#              Profile(user=instance,meta_key="wallet",meta_value=0),
#              Profile(user=instance,meta_key="carbonProduce",meta_value=0.0000)]
#             ) 
#     elif created and instance.role == "COMPANY" or instance.role == 'Company':
#         Profile.objects.bulk_create(
#             [Profile(user=instance,meta_key="companyName"),
#              Profile(user=instance,meta_key="phone"),
#              Profile(user=instance,meta_key="address"),
#              Profile(user=instance,meta_key="vatNumber"),
#              Profile(user=instance,meta_key="chairman")]
#             )
 
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    meta_key = models.CharField(max_length=50)
    meta_value = models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        unique_together = ['user','meta_key']

class Announcement(models.Model):
    title = models.CharField(max_length=50)
    upload_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(auto_now=True)
    context = models.TextField()
    isImportment = models.BooleanField(default = False)

