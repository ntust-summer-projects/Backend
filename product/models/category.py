from django.db import models
from rest_framework.exceptions import ValidationError



class CategoryManager(models.Manager):
    def __init__(self, categoryType):
        self.categoryType = categoryType
        super().__init__()
    
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(categoryType = self.categoryType)
        
class Category(models.Model):
    class CategoryType(models.TextChoices):
        MATERIAL = "MATERIAL",'material'
        PRODUCT = "PRODUCT", 'product' 
        
    baseType = CategoryType.MATERIAL
    
    name = models.CharField(max_length = 50, unique = True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name = 'childrens', blank = True, null = True )
    categoryType = models.CharField(max_length=50, choices= CategoryType.choices, default = CategoryType.MATERIAL, editable = False)
    
    def __str__(self):
        if self.parent:
            return f"{ self.parent }/{ self.name }"
        else:
            return self.name
    
    def save(self, *args, **kwargs):
        p = self.parent
        while p:
            if p.pk == self.pk or p.categoryType != self.categoryType:
                raise ValidationError("parent error")
            p = p.parent
        
        super().save(*args, **kwargs)
        
class ProductCategory(Category):
    baseType = Category.CategoryType.PRODUCT
    
    objects = CategoryManager(baseType)
    
    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        self.categoryType = self.baseType
        super().save(*args, **kwargs)
        
class MaterialCategory(Category):
    baseType = Category.CategoryType.MATERIAL
    
    objects = CategoryManager(baseType)
    
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        self.categoryType = self.baseType
        super().save(*args, **kwargs)
        
        
        
class Tag(models.Model):
    name = models.CharField(max_length=50, unique= True)
        
        
