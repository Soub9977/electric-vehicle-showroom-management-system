# Generated by Django 2.1.7 on 2022-07-15 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evapp', '0005_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='quotationnumber',
            field=models.ForeignKey(blank=True, db_column='quotationnumber', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evapp.Quotation'),
        ),
    ]
