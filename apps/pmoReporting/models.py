from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField
from datetime import datetime


class Entity(models.Model):
    Name = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)

    class Meta:
        verbose_name_plural = "entities"

class Category(models.Model):
    Name = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)

    class Meta:
        verbose_name_plural = "categories"

class SubCategory(models.Model):
    Name = models.CharField(max_length=50)  

    def __str__(self):
        return str(self.Name)

    class Meta:
        verbose_name_plural = "subcategories"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile_set')
    user_group = models.ManyToManyField(Entity)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "profiles"


class PmoData(models.Model):
    location = models.CharField(max_length=50)
    location_type = models.CharField(max_length=50)
    initiative_type = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    initiative_product = models.CharField(max_length=250)
    status = models.CharField(max_length=50)
    implementation_deadline = DateField(null=True, blank=True)
    creation_date = DateField(auto_now_add=True)
    initiative_year = models.CharField(max_length=5)
    actual_01 = models.FloatField(null=True, blank=True, default=0.0)
    actual_02 = models.FloatField(null=True, blank=True, default=0.0)
    actual_03 = models.FloatField(null=True, blank=True, default=0.0)
    actual_04 = models.FloatField(null=True, blank=True, default=0.0)
    actual_05 = models.FloatField(null=True, blank=True, default=0.0)
    actual_06 = models.FloatField(null=True, blank=True, default=0.0)
    actual_07 = models.FloatField(null=True, blank=True, default=0.0)
    actual_08 = models.FloatField(null=True, blank=True, default=0.0)
    actual_09 = models.FloatField(null=True, blank=True, default=0.0)
    actual_10 = models.FloatField(null=True, blank=True, default=0.0)
    actual_11 = models.FloatField(null=True, blank=True, default=0.0)
    actual_12 = models.FloatField(null=True, blank=True, default=0.0)
    budget_01 = models.FloatField(null=True, blank=True, default=0.0)
    budget_02 = models.FloatField(null=True, blank=True, default=0.0)
    budget_03 = models.FloatField(null=True, blank=True, default=0.0)
    budget_04 = models.FloatField(null=True, blank=True, default=0.0)
    budget_05 = models.FloatField(null=True, blank=True, default=0.0)
    budget_06 = models.FloatField(null=True, blank=True, default=0.0)
    budget_07 = models.FloatField(null=True, blank=True, default=0.0)
    budget_08 = models.FloatField(null=True, blank=True, default=0.0)
    budget_09 = models.FloatField(null=True, blank=True, default=0.0)
    budget_10 = models.FloatField(null=True, blank=True, default=0.0)
    budget_11 = models.FloatField(null=True, blank=True, default=0.0)
    budget_12 = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.initiative_product)

    def total_savings_actual(self):
        results = self.actual_01 + self.actual_02 + self.actual_03 + self.actual_04 + self.actual_05 + self.actual_06 + self.actual_07 + self.actual_08 + self.actual_09 + self.actual_10 + self.actual_11 + self.actual_12
        return round(results, 2)

    def total_savings_budget(self):
        results = self.budget_01 + self.budget_02 + self.budget_03 + self.budget_04 + self.budget_05 + self.budget_06 + self.budget_07 + self.budget_08 + self.budget_09 + self.budget_10 + self.budget_11 + self.budget_12
        return round(results, 2)
    
    def last_month_data(self):
        current_month = datetime.now().month
        if current_month == 1:
            budget = self.budget_12
            actual = self.actual_12
        elif current_month == 2:
            budget = self.budget_01
            actual = self.actual_01
        elif current_month == 3:
            budget = self.budget_02
            actual = self.actual_02
        elif current_month == 4:
            budget = self.budget_03
            actual = self.actual_03
        elif current_month == 5:
            budget = self.budget_04
            actual = self.actual_04
        elif current_month == 6:
            budget = self.budget_05
            actual = self.actual_05
        elif current_month == 7:
            budget = self.budget_06
            actual = self.actual_06
        elif current_month == 8:
            budget = self.budget_07
            actual = self.actual_07
        elif current_month == 9:
            budget = self.budget_08
            actual = self.actual_08
        elif current_month == 10:
            budget = self.budget_09
            actual = self.actual_09
        elif current_month == 11:
            budget = self.budget_10
            actual = self.actual_10
        elif current_month == 12:
            budget = self.budget_11
            actual = self.actual_11
        else:
            budget = None
            actual = None
        return [actual, budget]


    class Meta:
        verbose_name_plural = "pmo data"
