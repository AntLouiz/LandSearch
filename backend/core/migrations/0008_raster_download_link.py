# Generated by Django 2.1.5 on 2019-01-16 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190115_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='raster',
            name='download_link',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
    ]
