# Generated by Django 4.2.7 on 2023-11-29 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealSharing', '0002_order_profile_remove_meal_buyer_alter_meal_seller_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='shown',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='meal_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='can_buy',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='can_sell',
            field=models.BooleanField(default=False),
        ),
    ]
