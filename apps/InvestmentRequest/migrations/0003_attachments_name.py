# Generated by Django 3.2.4 on 2021-11-24 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvestmentRequest', '0002_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachments',
            name='name',
            field=models.CharField(default='test1', max_length=255),
            preserve_default=False,
        ),
    ]