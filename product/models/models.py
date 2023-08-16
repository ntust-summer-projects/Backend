from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from auditlog.models import LogEntry
from general.models import User
import requests
import django.utils.timezone as timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
import pandas as pd
import magic
import xml.etree.ElementTree as ET
import json
import codecs
import os

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
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique= True)

class Product(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'products', default = "11111111")
    name = models.CharField(max_length = 20)
    number = models.CharField(max_length = 50, blank = True)
    tag = models.ManyToManyField(Tag, related_name= 'products', blank=True)
    materials = models.ManyToManyField(to = 'Material', through = 'Component', related_name = 'products')
    carbonEmission = models.FloatField(editable = False, default = 0.0)
    last_update = models.DateTimeField(editable = False, auto_now_add=True)
    weight = models.FloatField(default = 0)
    
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

    def get_log(self):
        return LogEntry.objects.filter(Q(content_type = ContentType.objects.get_for_model(self), object_id = self.pk) |
                                       Q(content_type = ContentType.objects.get_for_model(Component), serialized_data__fields__product = self.pk))
        
    def get_component(self):
        return Component.objects.filter(product_id=self.id)


class Material(models.Model):
    name = models.CharField(max_length = 50, default = "未知")
    carbonEmission = models.FloatField(default = 0.0)
    unit = models.CharField(max_length = 50, null = True)
    
    def __str__(self):
        return f"{ self.name }"
    
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
    quantity = models.FloatField(default = 0.0)
    carbonEmission = models.FloatField(editable = False, default = 0.0)
    
    class Meta:
        unique_together = ['product', 'material']
    
    def __str__(self):
        return f"{ self.material } { self.quantity }"
    
    def getEmission(self):
        return self.quantity * self.material.carbonEmission
    
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
    
class UploadMaterial(models.Model):
    file = models.FileField(upload_to = 'uploads/%Y/%m/%d/')
    nameField = models.CharField(max_length = 50, default = 'name')
    coeField = models.CharField(max_length = 50, default = 'coe')
    unitField = models.CharField(max_length = 50, default = 'unit')
    dateTime = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
@receiver(post_delete, sender=UploadMaterial)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(pre_save, sender=UploadMaterial)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = UploadMaterial.objects.get(pk=instance.pk).file
    except UploadMaterial.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
        
@receiver(post_save, sender = UploadMaterial)
def updateMaterial(sender, instance, created, **kwargs):
    if not instance.file:
        return False
    
    magic_obj = magic.Magic()
    
    fileType = magic_obj.from_file(instance.file.path)
    
    def updateOrCreateMaterial(data):
        for index, row in data.iterrows():
            Material.objects.update_or_create({ 'name': row[instance.nameField], 'carbonEmission': float(row[instance.coeField]), 'unit': row[instance.unitField]}, name = row[instance.nameField])
    
    if "XML" in fileType:
        tree = ET.parse(instance.file.path)
        root = tree.getroot()
        for material in root:
            Material.objects.update_or_create({ 'name': material.find(instance.nameField).text, 'carbonEmission': float(material.find(instance.coeField).text), 'unit': material.find(instance.unitField).text}, name = material.find(instance.nameField).text)
    elif "Excel" in fileType:
        excel_sheet = pd.read_excel(instance.file.path, sheet_name = None, usecols = [instance.nameField, instance.coeField, instance.unitField])
        for sheet_name, sheet_data in excel_sheet.items():
            updateOrCreateMaterial(sheet_data)
    elif "CSV" in fileType:
        csv = pd.read_csv(instance.file.path, usecols = [instance.nameField, instance.coeField, instance.unitField])
        updateOrCreateMaterial(csv)
    else:
        try:
            file = pd.read_json(instance.file.path)
            updateOrCreateMaterial(file)
        except:
            file = codecs.open(instance.file.path, 'r', 'utf_8_sig')
            data = json.load(file)
            for row in data:
                Material.objects.update_or_create({ 'name': row[instance.nameField], 'carbonEmission': float(row[instance.coeField]), 'unit': row[instance.unitField]}, name = row[instance.nameField])
