# Generated by Django 3.0.2 on 2020-04-19 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_send_emails'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('created_on',)},
        ),
    ]