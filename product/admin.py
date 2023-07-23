from django.contrib import admin
from product.models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','description','carbonEmission','company')
    
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id','product','material','weight','carbonEmission')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('CName','EName','carbonEmission')
    
@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    list_display = ('id','name','carbonEmission')

@admin.register(LogT)
class LogTAdmin(admin.ModelAdmin):
    list_display = ('id','user','logType', 'distance', 'transportation','carbonEmission','timestamp')

@admin.register(LogI)
class LogIAdmin(admin.ModelAdmin):
    list_display = ('id','user','logType', 'product','amount','carbonEmission','timestamp')
