# Generated by Django 5.0.4 on 2024-09-23 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_expense', '0009_alter_pub_billmodel_current_eb_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub_billmodel',
            name='Total_Units',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pub_billmodel',
            name='total_amt',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
