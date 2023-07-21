# from django.db import models
# from django.db.models.signals import pre_delete, post_delete
# from django.dispatch import receiver
# from auditlog.registry import auditlog
# from auditlog.models import LogEntry
# from general.models import Company
# import requests

# def getComponyName(vatNumber):
#     url = f"https://data.gcis.nat.gov.tw/od/data/api/9D17AE0D-09B5-4732-A8F4-81ADED04B679?$format=json&$filter=Business_Accounting_NO eq { vatNumber }&$skip=0&$top=50"
#     response = requests.get(url)
#     if response.status_code == 200:
#         try:
#             data = response.json()
#             company_name = data[0]['Company_Name']
#             return company_name
#         except:
#             pass
#     return "Unknown"

# class Product(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name = 'products', default = "11111111")
#     name = models.CharField(max_length = 20)
#     description = models.TextField(blank = True)
#     materials = models.ManyToManyField(to = 'Material', through = 'Component', related_name = 'products')
#     carbonEmission = models.FloatField(editable = False, default = 0.0)
    
#     def getEmission(self):
#         emission = 0.0
#         try:
#             for component in self.component_set.all():
#                 emission += component.carbonEmission
            
#         except Product.DoesNotExist:
#             pass
#         return emission
    
#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         self.carbonEmission = self.getEmission()
#         self.getLog()
#         super().save(*args, **kwargs)

#     def getLog(self):
#         return LogEntry.objects.filter(object_id = self.pk)
    
# class Material(models.Model):
#     CName = models.CharField(max_length = 50, default = "未知")
#     EName = models.CharField(max_length = 50, default = "Unknown")
#     carbonEmission = models.FloatField(default = 0.0)
    
#     class Meta:
#         unique_together = ['CName', 'EName']
    
#     def __str__(self):
#         return self.CName
    
#     def save(self, *args, **kwargs):
#         try:
#             oldData = Material.objects.get(pk = self.pk)
            
#             if oldData.carbonEmission != self.carbonEmission:
#                 super().save(*args, **kwargs)
#                 for component in self.component_set.filter(material = self):
#                     component.save()
#                 return
        
#         except Material.DoesNotExist:
#             pass
#         super().save(*args, **kwargs)
            
    
# class Component(models.Model):
#     product = models.ForeignKey(to = 'Product', on_delete=models.CASCADE, default = 1)
#     material = models.ForeignKey(to = 'Material', on_delete=models.CASCADE, default = 1)
#     weight = models.FloatField(default = 0.0)
#     description = models.TextField(blank = True)
#     carbonEmission = models.FloatField(editable = False, default = 0.0)
    
#     class Meta:
#         unique_together = ['product', 'material']
    
#     def __str__(self):
#         return f"{ self.material } { self.weight }"
    
#     def getEmission(self):
#         return self.weight * self.material.carbonEmission
    
#     def save(self, *args, **kwargs):
#         self.carbonEmission = self.getEmission()
        
#         try:
#             oldData = Component.objects.get(pk = self.pk)
        
#             if oldData.carbonEmission != self.carbonEmission:
#                 super().save(*args, **kwargs)
#                 self.product.save()
#                 return
                
#         except Component.DoesNotExist:
#             super().save(*args, **kwargs)
#             self.product.save()
#             return
#         super().save(*args, **kwargs)
        
# @receiver(post_delete, sender = Component, dispatch_uid = 'component_delete_signal')
# def delete_carbonEmission(sender, instance, using, **kwargs):
#     instance.product.save()
    
# '''
# @receiver(pre_delete, sender = Record, dispatch_uid = 'record_delete_signal')
# def delete_wallet_point(sender, instance, using, **kwargs):
#     instance.user.wallet -= instance.point
#     instance.user.save()'''
    
# @receiver(pre_delete, sender = Product, dispatch_uid = 'product_delete_signal')
# def delete_photo(sender, instance, using, **kwargs):
#     instance.photo.delete(save = True)
    
    
# auditlog.register(Product,serialize_data=True)
# auditlog.register(Product.materials.through,serialize_data=True)




 

