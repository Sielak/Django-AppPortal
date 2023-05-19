from django.db import models
from django.contrib.auth.models import User

class SubjectGroup(models.Model):
    Name = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)

    class Meta:
        verbose_name_plural = "subject groups"

class Area(models.Model):
    Name = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)

    class Meta:
        verbose_name_plural = "areas"

class Group(models.Model):
    Name = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)

    class Meta:
        verbose_name_plural = "groups"

class Country(models.Model):
    Name = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)
    
    class Meta:
        verbose_name_plural = "countries"

class highlight_tracker_settings(models.Model):
    Name = models.CharField(max_length=50)  
    Value = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)

    class Meta:
        verbose_name_plural = "highlight tracker settings"

class highlight_data(models.Model):
    Subject_Group = models.CharField(max_length=50) 
    Improvement_Identified = models.CharField(max_length=50)
    Action_description = models.TextField(null=True, blank=True)
    Responsible_person = models.CharField(max_length=50, null=True, blank=True) 
    Completion_Date = models.DateField(null=True, blank=True)
    Action_status = models.CharField(max_length=50, null=True, blank=True) 
    Comments = models.TextField(null=True, blank=True)
    row_Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    row_Area = models.ForeignKey(Area, on_delete=models.CASCADE)
    row_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    row_Year = models.CharField(max_length=10) 

    def __str__(self):
        return str(self.Subject_Group)
    
    class Meta:
        verbose_name_plural = "highlight data"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_group = models.ManyToManyField(Group)
    user_area = models.ManyToManyField(Area)
    user_country = models.ManyToManyField(Country)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = "profiles"

