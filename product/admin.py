from django.contrib import admin
from product.models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','number','carbonEmission','company', 'last_update')
    
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id','product','material','weight','carbonEmission')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name','carbonEmission')
    
@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    list_display = ('id','name','carbonEmission')

@admin.register(LogT)
class LogTAdmin(admin.ModelAdmin):
    list_display = ('id','user','logType', 'distance', 'transportation','carbonEmission','timestamp')

@admin.register(LogI)
class LogIAdmin(admin.ModelAdmin):
    list_display = ('id','user','logType', 'product','amount','carbonEmission','timestamp')
    
admin.site.register(AbstractLog)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.filter(categoryType = ProductCategory.baseType)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.filter(categoryType = MaterialCategory.baseType)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UploadMaterial)