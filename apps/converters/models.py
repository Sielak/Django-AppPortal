from django.db import models


class AldiMatrix(models.Model):
    jeeves_code = models.CharField(max_length=50)
    unit_cost = models.FloatField()
    type = models.CharField(max_length=10)

    e_850 = models.IntegerField()
    e_900 = models.IntegerField()
    e_940 = models.IntegerField()
    e_960 = models.IntegerField()
    e_990_1006 = models.IntegerField()
    e_v2_1125_1140 = models.IntegerField()
    e_v2_1254_1315 = models.IntegerField()

    erh_850 = models.IntegerField()
    erh_900 = models.IntegerField()
    erh_940 = models.IntegerField()
    erh_960 = models.IntegerField()
    erh_990_1006 = models.IntegerField()
    erh_v2_1125_1140 = models.IntegerField()
    erh_v2_1254_1315 = models.IntegerField()

    s_850 = models.IntegerField()
    s_900 = models.IntegerField()
    s_940 = models.IntegerField()
    s_960 = models.IntegerField()
    s_990_1006 = models.IntegerField()
    s_v2_1125_1140 = models.IntegerField()
    s_v2_1254_1315 = models.IntegerField()

    srh_850 = models.IntegerField()
    srh_900 = models.IntegerField()
    srh_940 = models.IntegerField()
    srh_960 = models.IntegerField()
    srh_990_1006 = models.IntegerField()
    srh_v2_1125_1140 = models.IntegerField()
    srh_v2_1254_1315 = models.IntegerField()

    w_850 = models.IntegerField()
    w_900 = models.IntegerField()
    w_940 = models.IntegerField()
    w_960 = models.IntegerField()
    w_990_1006 = models.IntegerField()
    w_v2_1125_1140 = models.IntegerField()
    w_v2_1254_1315 = models.IntegerField()

    wrh_850 = models.IntegerField()
    wrh_900 = models.IntegerField()
    wrh_940 = models.IntegerField()
    wrh_960 = models.IntegerField()
    wrh_990_1006 = models.IntegerField()
    wrh_v2_1125_1140 = models.IntegerField()
    wrh_v2_1254_1315 = models.IntegerField()

    def __str__(self):
        return self.jeeves_code
