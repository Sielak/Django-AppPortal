from os import name
from django.db import models

class ApiLogs(models.Model):
    timestamp = models.DateTimeField()
    customer = models.CharField(max_length=100)
    type = models.TextField()
    name = models.TextField()
    result = models.TextField()

    class Meta:
        verbose_name = "API log"
        verbose_name_plural = "API logs"
