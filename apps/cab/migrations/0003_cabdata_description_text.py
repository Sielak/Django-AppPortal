# Generated by Django 3.2.4 on 2021-08-24 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0002_cabdata_est_deliv_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabdata',
            name='description_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]