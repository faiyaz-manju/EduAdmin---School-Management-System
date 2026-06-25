from django.db import models

# Create your models here.
class ExpenditureModel(models.Model):
    category = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.BigIntegerField()
    date = models.DateField()
    
    def __str__(self):
        return self.category