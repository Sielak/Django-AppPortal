# Generated by Django 3.2.4 on 2021-11-23 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvestmentRequest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvestmentRequest.investmentheader')),
            ],
            options={
                'verbose_name_plural': 'attachments',
            },
        ),
    ]
