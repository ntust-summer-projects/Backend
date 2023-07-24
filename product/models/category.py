from django.db import models
from product.models.abstract import AbstractCategory

'''
    create category:
        CategoryManager.create(categoryType,name, parent = null)
'''
class CategoryType(models.TextChoices):
        MATERIAL = "MATERIAL",'material'
        PRODUCT = "PRODUCT", 'product' 

class CategoryManager(models.Manager):   
    def create(*args, **kwargs):
        match kwargs.pop('categoryType',None):
            case CategoryType.MATERIAL:
                MaterialCategory.objects.create(*args, **kwargs)
            case CategoryType.PRODUCT:
                ProductCategory.objects.create(*args, **kwargs)

class MaterialCategory(AbstractCategory):
    parent = models.ForeignKey(to = 'self', on_delete=models.CASCADE, related_name = 'submcategorys', blank = True, null = True)
    
class ProductCategory(AbstractCategory):
    parent = models.ForeignKey(to = 'self', on_delete=models.CASCADE, related_name = 'subpcategorys', blank = True, null = True)
    
    