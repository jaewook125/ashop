# Generated by Django 2.0.4 on 2018-04-23 04:27

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20180419_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='meta',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
    ]