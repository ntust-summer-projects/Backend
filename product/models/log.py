from django.db import models
from django.db.models.query import QuerySet
from general.models import User
from product.models import Transportation, Product
from auditlog.registry import auditlog
            
class LogManager(models.Manager):
    def create(*args, **kwargs):
        t = kwargs.pop('logType',None)
        match t:
            case AbstractLog.LogType.TRANSPORTATION:
                return LogT.objects.create(**kwargs)
            case AbstractLog.LogType.ITEM:
                return LogI.objects.create(**kwargs)
            case _:
                raise Exception("LogType not found")
            
    '''def get_queryset(self,*args,**kwargs):
        match kwargs.pop('logType',None):
            case AbstractLog.LogType.TRANSPORTATION:
                return LogT.objects.get_queryset(*args, **kwargs)
            case AbstractLog.LogType.ITEM:
                return LogI.objects.get_queryset(*args, **kwargs)
            case _:
                return super().get_queryset(*args, **kwargs)'''
            
    def all(self, *args, **kwargs):
        match kwargs.pop('logType',None):
            case AbstractLog.LogType.TRANSPORTATION:
                return LogT.objects.all(*args, **kwargs)
            case AbstractLog.LogType.ITEM:
                return LogI.objects.all(*args, **kwargs)
            case _:
                return super().all(*args, **kwargs)
    def filter(self, *args, **kwargs):
        match kwargs.pop('logType',None):
            case AbstractLog.LogType.TRANSPORTATION:
                return LogT.objects.filter(*args, **kwargs)
            case AbstractLog.LogType.ITEM:
                return LogI.objects.filter(*args, **kwargs)
            case _:
                return super().filter(*args, **kwargs)
            
                    
class AbstractLog(models.Model):
    class LogType(models.TextChoices):
        TRANSPORTATION = "TRANSPORTATION", 'transportation'
        ITEM = "ITEM", 'item'
    
    baseType = LogType.TRANSPORTATION
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logType = models.CharField(max_length=50, choices=LogType.choices,default = LogType.TRANSPORTATION, editable = False)
    carbonEmission = models.FloatField(editable = False, default = 0.0)
    timestamp = models.DateTimeField(
        auto_now = True,
        db_index=True,
    )
    
    objects = LogManager()
    
    def save(self, *args, **kwargs):
        LogManager.create(user = self.user, logType = self.logType, **kwargs)

    def _save(self, *args, **kwargs):
        self.logType = self.baseType
        if not kwargs.get('force_insert', False):
            print("Warning : log maybe be changed !")
        super().save(*args,**kwargs)
        
    
class LogT(AbstractLog):
    distance = models.FloatField(blank = True, default = 0.0)
    transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE, related_name = 'logs', default = 1)
    
    baseType = AbstractLog.LogType.TRANSPORTATION
        
    class Meta:
        verbose_name = 'Transportation Log'
        verbose_name_plural = 'Transportation Logs'
        
    def getEmission(self):
        return self.distance * self.transportation.carbonEmission
        
    def __str__(self): 
        return f"{ self.pk }"
    
    def save(self, *args, **kwargs):
        self.carbonEmission = self.getEmission()
        super()._save(*args, **kwargs)
    
class LogI(AbstractLog):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default = 1)
    amount = models.PositiveBigIntegerField(default = 0)
    
    baseType = AbstractLog.LogType.ITEM
    
    class Meta:
        verbose_name = 'Item Log'
        verbose_name_plural = 'Item Logs'
        
    def getEmission(self):
        return self.amount * self.product.carbonEmission
        
    def save(self, *args, **kwargs):
        self.carbonEmission = self.getEmission()
        super()._save(*args, **kwargs)
    
auditlog.register(Product,serialize_data=True)
auditlog.register(Product.materials.through,serialize_data=True)