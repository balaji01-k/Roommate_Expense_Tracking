# Generated by Django 5.0.4 on 2024-09-21 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_expense', '0004_remove_pub_billmodel_water_utility_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pub_billmodel',
            name='Current_month_EB_Total_Reading',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='pub_billmodel',
            name='EB_Unit_Cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='pub_billmodel',
            name='GST',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='pub_billmodel',
            name='Previous_month_EB_Total_Reading',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='pub_billmodel',
            name='Refuse_Removal_Amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
