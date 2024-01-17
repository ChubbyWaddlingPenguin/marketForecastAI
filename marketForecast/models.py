from django.db import models

class MyData(models.Model):
    symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    open = models.CharField(max_length=15)
    high = models.CharField(max_length=15)
    low = models.CharField(max_length=15)
    close = models.CharField(max_length=15)
    volume = models.IntegerField()

    class Meta:
        managed = False  
        db_table = 'OUTPUT'  