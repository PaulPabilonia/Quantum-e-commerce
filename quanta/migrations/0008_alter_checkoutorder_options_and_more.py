# Generated by Django 4.0.3 on 2022-05-08 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quanta', '0007_remove_checkoutorder_products_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkoutorder',
            options={},
        ),
        migrations.RemoveField(
            model_name='checkoutorder',
            name='expected_delivery',
        ),
    ]
