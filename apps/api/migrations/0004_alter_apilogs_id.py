# Generated by Django 3.2.4 on 2021-06-18 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210402_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apilogs',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
