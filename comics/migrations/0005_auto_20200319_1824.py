# Generated by Django 3.0.2 on 2020-03-19 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0004_auto_20200319_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comicpanel',
            name='chapter',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comicpanel',
            name='page',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
