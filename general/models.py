from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as timezone

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        NORMAL = "NORMAL", 'Normal'
        COMPANY = "COMPANY", 'Company'
        
    base_role = Role.ADMIN
    
    phone = models.CharField(max_length=50,null=True,blank=True)
    
    role = models.CharField(max_length=50, choices=Role.choices,default = Role.ADMIN)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args,**kwargs)
 
class NormalManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        result = super().get_queryset(*args,**kwargs).filter(role=User.Role.NORMAL)
        return result
        
class Normal(User):
    
    base_role = User.Role.NORMAL
    
    normal = NormalManager()
    
    @property
    def profile(self):
        return self.normalprofile
    
    class Meta:
        proxy = True

@receiver(post_save, sender=Normal)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "NORMAL":
        NormalProfile.objects.create(user=instance)

class NormalProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    wallet = models.PositiveBigIntegerField(editable=False,default=0)
    carbonProduce = models.DecimalField(max_digits=20,decimal_places=4,default=0.0000)

    

class CompanyManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        result = super().get_queryset(*args,**kwargs).filter(role = User.Role.COMPANY)
        return result
        
class Company(User):
    
    base_role = User.Role.COMPANY
    
    company = CompanyManager()
    
    @property
    def profile(self):
        return self.companyprofile
    
    class Meta:
        proxy = True

@receiver(post_save, sender=Company)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "COMPANY":
        CompanyProfile.objects.create(user=instance)

class CompanyProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    companyName = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    vitNumber = models.CharField(max_length = 8, unique = True, default = "00000000", primary_key=True)
    chairman = models.CharField(max_length=50,null=True,blank=True)

class Announcement(models.Model):
    title = models.CharField(max_length=50)
    upload_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(auto_now=True)
    context = models.TextField()