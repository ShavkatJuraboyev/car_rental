# Generated by Django 4.2.11 on 2024-05-02 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carrental', '0006_carrentai'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrentai',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='carrentai',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CarRentai', to='carrental.carrentai'),
        ),
    ]
