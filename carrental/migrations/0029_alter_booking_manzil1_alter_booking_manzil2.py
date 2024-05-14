# Generated by Django 4.2.11 on 2024-05-13 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carrental', '0028_alter_booking_manzil1_alter_booking_manzil2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='manzil1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carrental.manzil1'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='manzil2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carrental.manzil2'),
        ),
    ]
