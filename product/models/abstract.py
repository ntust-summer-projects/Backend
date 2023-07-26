from django.db import models
from rest_framework.exceptions import ValidationError

class AbstractCategory(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    parent = None
    
    class Meta:
        abstract = True
    
    def __str__(self):
        if self.parent:
            return f"{ self.parent }/{ self.name }"
        else:
            return self.name
    
    def save(self, *args, **kwargs):
        if self.pk:
            p = self.parent
            while p:
                if p.pk == self.pk:
                    raise ValidationError("parent error")
                p = p.parent
        super().save(*args, **kwargs)


        
        
             
        
                

    
