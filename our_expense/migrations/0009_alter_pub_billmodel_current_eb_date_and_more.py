# Generated by Django 5.0.4 on 2024-09-21 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_expense', '0008_alter_pub_billmodel_current_eb_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pub_billmodel',
            name='Current_EB_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pub_billmodel',
            name='Previous_EB_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
