# Generated by Django 2.1.5 on 2019-01-20 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190116_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordinates',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='raster',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='scrapingorder',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='shapefile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]