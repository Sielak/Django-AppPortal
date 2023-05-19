from django.db import models
from django.contrib.auth.models import User
from django.db.models import Case, F, IntegerField, Sum, Value, When


def get_name(self):
    return '{} {}'.format(self.first_name, self.last_name)

User.add_to_class("__str__", get_name)

class CashFlowGroupNames(models.Model):
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.group_name)
    
    class Meta:
        verbose_name_plural = "cash flow group names"

class CashFlowNames(models.Model):
    row_number = models.IntegerField()
    name = models.CharField(max_length=50)
    cash_flow_group = models.ForeignKey(CashFlowGroupNames, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "cash flow names"


class Companies(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()

    approval_level_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_1', null=True, blank=True)
    approval_level_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_2', null=True, blank=True)
    approval_level_3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_3', null=True, blank=True)
    approval_level_4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_4', null=True, blank=True)
    approval_level_5 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_5', null=True, blank=True)
    approval_level_6 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_6', null=True, blank=True)
    approval_level_7 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_7', null=True, blank=True)
    approval_level_8 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_8', null=True, blank=True)
    approval_level_9 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_level_9', null=True, blank=True)
    approval_level_1_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_2_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_3_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_4_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_5_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_6_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_7_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_8_desc = models.CharField(max_length=50, null=True, blank=True)
    approval_level_9_desc = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Companies"

class InvestmentHeader(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    project = models.CharField(max_length=50)
    requested_amount = models.IntegerField()
    why = models.TextField(null=True, blank=True)
    what = models.TextField(null=True, blank=True)
    how = models.TextField(null=True, blank=True)
    alternative = models.TextField(null=True, blank=True)
    env_impact = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    depreciation_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by')

    def __str__(self):
        return str(self.name)
    
    def cash_flow(self):
        year1 = self.investmentrow_set.aggregate(Sum('year_01'))['year_01__sum'] or 0
        year2 = self.investmentrow_set.aggregate(Sum('year_02'))['year_02__sum'] or 0
        year3 = self.investmentrow_set.aggregate(Sum('year_03'))['year_03__sum'] or 0
        year4 = self.investmentrow_set.aggregate(Sum('year_04'))['year_04__sum'] or 0
        year5 = self.investmentrow_set.aggregate(Sum('year_05'))['year_05__sum'] or 0
        cash_flow_data = {
            "normal": {
                "year1": year1,
                "year2": year2,
                "year3": year3,
                "year4": year4,
                "year5": year5,
            },
            "accumulated": {
                "year1": year1,
                "year2": year1 + year2,
                "year3": year1 + year2 + year3,
                "year4": year1 + year2 + year3 + year4,
                "year5": year1 + year2 + year3 + year4 + year5,
            }        
        }
        return cash_flow_data

    def approval_data(self):
        approvals = self.approvaldata_set.all()
        approval_data = [
            {"name": self.company.approval_level_1, "desc": self.company.approval_level_1_desc, "status": approvals[0].level_1_status, "date": approvals[0].level_1_date},
            {"name": self.company.approval_level_2, "desc": self.company.approval_level_2_desc, "status": approvals[0].level_2_status, "date": approvals[0].level_2_date},
            {"name": self.company.approval_level_3, "desc": self.company.approval_level_3_desc, "status": approvals[0].level_3_status, "date": approvals[0].level_3_date},
            {"name": self.company.approval_level_4, "desc": self.company.approval_level_4_desc, "status": approvals[0].level_4_status, "date": approvals[0].level_4_date},
            {"name": self.company.approval_level_5, "desc": self.company.approval_level_5_desc, "status": approvals[0].level_5_status, "date": approvals[0].level_5_date},
            {"name": self.company.approval_level_6, "desc": self.company.approval_level_6_desc, "status": approvals[0].level_6_status, "date": approvals[0].level_6_date},
            {"name": self.company.approval_level_7, "desc": self.company.approval_level_7_desc, "status": approvals[0].level_7_status, "date": approvals[0].level_7_date},
            {"name": self.company.approval_level_8, "desc": self.company.approval_level_8_desc, "status": approvals[0].level_8_status, "date": approvals[0].level_8_date},
            {"name": self.company.approval_level_9, "desc": self.company.approval_level_9_desc, "status": approvals[0].level_9_status, "date": approvals[0].level_9_date}
        ]
        return approval_data

    def payback_time(self):
        year1_positive = self.investmentrow_set.filter(year_01__gt=0).aggregate(Sum('year_01'))['year_01__sum'] or 0
        year2_positive = self.investmentrow_set.filter(year_02__gt=0).aggregate(Sum('year_02'))['year_02__sum'] or 0
        year3_positive = self.investmentrow_set.filter(year_03__gt=0).aggregate(Sum('year_03'))['year_03__sum'] or 0
        year4_positive = self.investmentrow_set.filter(year_04__gt=0).aggregate(Sum('year_04'))['year_04__sum'] or 0
        year5_positive = self.investmentrow_set.filter(year_05__gt=0).aggregate(Sum('year_05'))['year_05__sum'] or 0

        year1_negative = self.investmentrow_set.filter(year_01__lt=0).aggregate(Sum('year_01'))['year_01__sum'] or 0
        year2_negative = self.investmentrow_set.filter(year_02__lt=0).aggregate(Sum('year_02'))['year_02__sum'] or 0
        year3_negative = self.investmentrow_set.filter(year_03__lt=0).aggregate(Sum('year_03'))['year_03__sum'] or 0
        year4_negative = self.investmentrow_set.filter(year_04__lt=0).aggregate(Sum('year_04'))['year_04__sum'] or 0
        year5_negative = self.investmentrow_set.filter(year_05__lt=0).aggregate(Sum('year_05'))['year_05__sum'] or 0

        total_negative = year1_negative + year2_negative + year3_negative + year4_negative + year5_negative

        try:
            total_year_1 = year1_positive - (total_negative * -1)
            if total_year_1 < 0:
                total_year_2 = year2_positive - (total_year_1 * -1)
                if total_year_2 < 0:
                    total_year_3 = year3_positive - (total_year_2 * -1)
                    if total_year_3 < 0:
                        total_year_4 = year4_positive - (total_year_3 * -1)
                        if total_year_4 < 0:
                            ratio = ((total_year_4 * -1) / year5_positive) + 4
                        else:
                            ratio = ((total_year_3 * -1) / year4_positive) + 3
                    else:
                        ratio = ((total_year_2 * -1) / year3_positive) + 2
                else:
                    ratio = ((total_year_1 * -1) / year2_positive) + 1
            else:
                ratio = ((total_negative * -1) / year1_positive)
        except ZeroDivisionError:
            ratio = 0
        
        return round(ratio, 2)

    def approval_status(self):
        approvals = self.approvaldata_set.all()
        approval_data = [
            approvals[0].level_1_status,
            approvals[0].level_2_status,
            approvals[0].level_3_status,
            approvals[0].level_4_status,
            approvals[0].level_5_status,
            approvals[0].level_6_status,
            approvals[0].level_7_status,
            approvals[0].level_8_status,
            approvals[0].level_9_status
        ]
        approval_data = set(approval_data)
        approval_data.discard('not_used')
        if "Rejected" in approval_data:
            return 'Rejected'
        elif len(approval_data) == 1 and list(approval_data)[0] is None:
            return 'Open'
        elif ("Approved" in approval_data or "Reviewed" in approval_data) and None in approval_data:
            return 'In Progress'
        else:
            return 'Completed'

    class Meta:
        verbose_name_plural = "investment headers"

class InvestmentRow(models.Model):
    header = models.ForeignKey(InvestmentHeader, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    type_number = models.IntegerField()
    type_group = models.CharField(max_length=50)
    year_01 = models.IntegerField(null=True, blank=True)
    year_02 = models.IntegerField(null=True, blank=True)
    year_03 = models.IntegerField(null=True, blank=True)
    year_04 = models.IntegerField(null=True, blank=True)
    year_05 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{0}-{1}".format(self.header.name, self.type)
    
    class Meta:
        verbose_name_plural = "investment rows"

class ApprovalData(models.Model):
    header = models.ForeignKey(InvestmentHeader, on_delete=models.CASCADE)
    level_1_status = models.CharField(max_length=50, null=True, blank=True)
    level_2_status = models.CharField(max_length=50, null=True, blank=True)
    level_3_status = models.CharField(max_length=50, null=True, blank=True)
    level_4_status = models.CharField(max_length=50, null=True, blank=True)
    level_5_status = models.CharField(max_length=50, null=True, blank=True)
    level_6_status = models.CharField(max_length=50, null=True, blank=True)
    level_7_status = models.CharField(max_length=50, null=True, blank=True)
    level_8_status = models.CharField(max_length=50, null=True, blank=True)
    level_9_status = models.CharField(max_length=50, null=True, blank=True)

    level_1_date = models.DateField(null=True, blank=True)
    level_2_date = models.DateField(null=True, blank=True)
    level_3_date = models.DateField(null=True, blank=True)
    level_4_date = models.DateField(null=True, blank=True)
    level_5_date = models.DateField(null=True, blank=True)
    level_6_date = models.DateField(null=True, blank=True)
    level_7_date = models.DateField(null=True, blank=True)
    level_8_date = models.DateField(null=True, blank=True)
    level_9_date = models.DateField(null=True, blank=True)

    def truncate_data(self):
        if self.level_1_status == 'not_used':
            self.level_1_status = None
            self.level_1_date = None
        if self.level_2_status == 'not_used':
            self.level_2_status = None
            self.level_2_date = None
        if self.level_3_status == 'not_used':
            self.level_3_status = None
            self.level_3_date = None
        if self.level_4_status == 'not_used':
            self.level_4_status = None
            self.level_4_date = None
        if self.level_5_status == 'not_used':
            self.level_5_status = None
            self.level_5_date = None
        if self.level_6_status == 'not_used':
            self.level_6_status = None
            self.level_6_date = None
        if self.level_7_status == 'not_used':
            self.level_7_status = None
            self.level_7_date = None
        if self.level_8_status == 'not_used':
            self.level_8_status = None
            self.level_8_date = None
        if self.level_9_status == 'not_used':
            self.level_9_status = None
            self.level_9_date = None

    def __str__(self):
        return self.header.name
    
    class Meta:
        verbose_name_plural = "approval data"

class Attachments(models.Model):
    header = models.ForeignKey(InvestmentHeader, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    def __str__(self):
        return "{0}-{1}".format(self.header.name, self.name)
    
    class Meta:
        verbose_name_plural = "attachments"
