# Generated by Django 5.0.3 on 2024-03-30 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growlivapp', '0005_alter_business_managers_remove_business_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='address_1',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='business',
            name='address_2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
