# Generated by Django 3.2.4 on 2021-11-30 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvestmentRequest', '0006_rename_deadline_investmentheader_depreciation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentrow',
            name='year_01',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investmentrow',
            name='year_02',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investmentrow',
            name='year_03',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investmentrow',
            name='year_04',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investmentrow',
            name='year_05',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]