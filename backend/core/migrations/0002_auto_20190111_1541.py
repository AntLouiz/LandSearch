# Generated by Django 2.1.5 on 2019-01-11 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapingorder',
            name='is_scraped',
        ),
        migrations.AddField(
            model_name='scrapingorder',
            name='status',
            field=models.CharField(choices=[('Waiting', 'waiting'), ('Scraping', 'scraping'), ('Finished', 'finished'), ('No result', 'no_result')], default='waiting', max_length=100),
            preserve_default=False,
        ),
    ]
