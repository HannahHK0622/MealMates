# Generated by Django 4.2.7 on 2023-11-29 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealSharing', '0003_meal_shown_alter_meal_meal_id_alter_profile_can_buy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
