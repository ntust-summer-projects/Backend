from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from auditlog.models import LogEntry
from general.models import User
import requests
import django.utils.timezone as timezone
from .category import Category
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

def getComponyName(vatNumber):
    url = f"https://data.gcis.nat.gov.tw/od/data/api/9D17AE0D-09B5-4732-A8F4-81ADED04B679?$format=json&$filter=Business_Accounting_NO eq { vatNumber }&$skip=0&$top=50"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            company_name = data[0]['Company_Name']
            return company_name
        except:
            pass
    return "Unknown"
        
class Product(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'products', default = "11111111")
    name = models.CharField(max_length = 20)
    number = models.CharField(max_length = 50, blank = True)
    category = models.ForeignKey(Category, limit_choices_to={'categoryType': Category.CategoryType.PRODUCT}, on_delete=models.SET_NULL, related_name = 'products', blank = True, null = True)
    materials = models.ManyToManyField(to = 'Material', through = 'Component', related_name = 'products')
    carbonEmission = models.FloatField(editable = False, default = 0.0)
    last_update = models.DateTimeField(editable = False, auto_now_add=True)
    
    def getEmission(self):
        emission = 0.0
        try:
            for component in self.component_set.all():
                emission += component.carbonEmission
            
        except Product.DoesNotExist:
            pass
        return emission
    
    def __str__(self):
        #self.getEmission()
        return self.name
    
    def save(self, *args, **kwargs):
        if kwargs.pop('updateTime', True):
            self.last_update = timezone.now()
        if self.pk:
            self.carbonEmission = self.getEmission()
        super().save(*args, **kwargs)
        #self.getLog()

    def getLog(self):
        return LogEntry.objects.filter(Q(content_type = ContentType.objects.get_for_model(self), object_id = self.pk) |
                                       Q(content_type = ContentType.objects.get_for_model(Component), serialized_data__fields__product = self.pk))

    
class Material(models.Model):
    CName = models.CharField(max_length = 50, default = "未知")
    EName = models.CharField(max_length = 50, default = "Unknown")
    carbonEmission = models.FloatField(default = 0.0)
    category = models.ForeignKey(Category, limit_choices_to={'categoryType': Category.CategoryType.MATERIAL}, on_delete=models.SET_NULL, related_name = 'materials', blank = True, null = True)
    
    class Meta:
        unique_together = ['CName', 'EName']
    
    def __str__(self):
        return f"{ self.EName } { self.CName }"
    
    def save(self, *args, **kwargs):
        if self.pk and Material.objects.get(pk = self.pk).carbonEmission != self.carbonEmission:
            kwargs['force_update'] = True
            super().save(*args, **kwargs)
            for component in self.component_set.filter(material = self):
                component.save(force_update = True, updateTime = False)
        else:  
            super().save(*args, **kwargs)
       
class Transportation(models.Model):
    name = models.CharField(max_length = 20, unique = True)
    carbonEmission = models.FloatField(default = 0.0)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk and Transportation.objects.get(pk = self.pk).carbonEmission != self.carbonEmission:
            super().save(*args, **kwargs)
            for log in self.logtprofile_set.filter(transportation = self):
                log.save()
        else:
            super().save(*args, **kwargs)     
    
class Component(models.Model):
    product = models.ForeignKey(to = 'Product', on_delete=models.CASCADE, default = 1)
    material = models.ForeignKey(to = 'Material', on_delete=models.CASCADE, default = 1)
    weight = models.FloatField(default = 0.0)
    description = models.TextField(blank = True)
    carbonEmission = models.FloatField(editable = False, default = 0.0)
    
    class Meta:
        unique_together = ['product', 'material']
    
    def __str__(self):
        return f"{ self.material } { self.weight }"
    
    def getEmission(self):
        return self.weight * self.material.carbonEmission
    
    def save(self, *args, **kwargs):
        self.carbonEmission = self.getEmission()
        updateTime = kwargs.pop('updateTime',True)
        if self.pk and Component.objects.get(pk = self.pk).carbonEmission == self.carbonEmission:
            kwargs['force_update'] = True
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            self.product.save(force_update = True, updateTime = updateTime)
        
@receiver(post_delete, sender = Component, dispatch_uid = 'component_delete_signal')
def update_carbonEmission(sender, instance, using, **kwargs):
    instance.product.save(force_update = True)
