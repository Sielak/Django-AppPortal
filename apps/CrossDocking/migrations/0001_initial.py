# Generated by Django 3.2.4 on 2021-06-18 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrossDockingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(max_length=50)),
                ('po_status', models.CharField(blank=True, max_length=50, null=True)),
                ('po_supplier', models.CharField(blank=True, max_length=100, null=True)),
                ('confirmation_date', models.DateField(blank=True, null=True)),
                ('path2file', models.CharField(blank=True, max_length=255, null=True)),
                ('delivery_number', models.CharField(blank=True, max_length=50, null=True)),
                ('pallet_count', models.IntegerField(blank=True, null=True)),
                ('row_status', models.CharField(blank=True, max_length=50, null=True)),
                ('packages', models.IntegerField(blank=True, null=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('shipment_date', models.DateField(blank=True, null=True)),
                ('file_uploaded', models.BooleanField(default=False)),
                ('pallet_location', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, default=0.0, null=True)),
            ],
            options={
                'verbose_name_plural': 'cross docking logs',
            },
        ),
        migrations.CreateModel(
            name='CrossDockingParams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Param_Name', models.CharField(max_length=50, unique=True)),
                ('Param_Value_int', models.FloatField(blank=True, null=True)),
                ('Param_Value_string', models.CharField(blank=True, max_length=100, null=True)),
                ('Param_Value_Description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'cross docking params',
            },
        ),
    ]