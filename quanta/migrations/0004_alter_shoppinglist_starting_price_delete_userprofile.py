# Generated by Django 4.0.3 on 2022-04-27 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quanta', '0003_user_pictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='starting_price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
