# Generated by Django 4.2.11 on 2024-05-13 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrental', '0022_alter_carrentai_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_comentary',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
