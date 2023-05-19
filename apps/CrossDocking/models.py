from django.db import models
import datetime


def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date

class CrossDockingParams(models.Model):
    Param_Name = models.CharField(max_length=50, unique=True)
    Param_Value_int = models.FloatField(null=True, blank=True) 
    Param_Value_string = models.CharField(max_length=100, null=True, blank=True) 
    Param_Value_Description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.Param_Name

    class Meta:
        verbose_name_plural = "cross docking params"


class CrossDockingLogs(models.Model):
    po_number = models.CharField(max_length=50)
    po_status = models.CharField(max_length=50, null=True, blank=True)
    po_supplier = models.CharField(max_length=100, null=True, blank=True)
    confirmation_date = models.DateField(null=True, blank=True)
    path2file = models.CharField(max_length=255, null=True, blank=True)
    delivery_number =  models.CharField(max_length=50, null=True, blank=True)
    pallet_count = models.IntegerField(null=True, blank=True)
    row_status = models.CharField(max_length=50, null=True, blank=True)
    packages = models.IntegerField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    shipment_date = models.DateField(null=True, blank=True)
    file_uploaded = models.BooleanField(default=False)
    pallet_location = models.TextField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.po_number)

    def calculate_price(self):
        try:
            delta = (self.shipment_date - self.delivery_date).days
            price_multiplication = CrossDockingParams.objects.filter(Param_Name='Price Multiplication')[0]
            InOut_price = CrossDockingParams.objects.filter(Param_Name='InOut price')[0].Param_Value_int
            price = ((delta * price_multiplication.Param_Value_int) + (2 * InOut_price)) * (self.pallet_count + self.packages)
            price = round(price, 2)
        except TypeError:
            price = 0
        
        return price

    def delayed_delivery(self):
        result = False
        deadline_date = date_by_adding_business_days(datetime.date.today(), 6)
        if self.confirmation_date < deadline_date and self.po_status == 'Order acknowledged' and self.row_status == 'Waiting for delivery':
            result = True
        return result

    class Meta:
        verbose_name_plural = "cross docking logs"