# Generated by Django 3.2.4 on 2021-08-12 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabdata',
            name='est_deliv_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
