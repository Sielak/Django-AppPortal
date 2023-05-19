from django.db import models


class CabData(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    step = models.CharField(max_length=50, null=True, blank=True)
    stream = models.CharField(max_length=200, null=True, blank=True)
    feature = models.CharField(max_length=50, null=True, blank=True)
    est_dev_hrs = models.FloatField(null=True, blank=True)
    est_cost_sek = models.FloatField(null=True, blank=True)
    est_deliv_date = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    hl_payer = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    description_text = models.TextField(null=True, blank=True)

    def hl_payer_list(self):
        return self.hl_payer.split("#")

    class Meta:
        verbose_name = "CAB data"
        verbose_name_plural = "CAB data"
