# Generated by Django 3.2.4 on 2021-11-30 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InvestmentRequest', '0005_investmentheader_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investmentheader',
            old_name='deadline',
            new_name='depreciation_date',
        ),
    ]
