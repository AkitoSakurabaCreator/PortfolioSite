# Generated by Django 4.1.3 on 2023-01-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='buildingname',
            field=models.CharField(blank=True, max_length=30, verbose_name='建物名'),
        ),
    ]
