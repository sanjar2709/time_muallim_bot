# Generated by Django 4.1.3 on 2022-11-13 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0002_post_send_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='channel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
