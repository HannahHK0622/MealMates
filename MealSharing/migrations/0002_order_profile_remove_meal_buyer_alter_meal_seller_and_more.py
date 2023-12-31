# Generated by Django 4.2.7 on 2023-11-27 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MealSharing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date_bought', models.DateField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Buyer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(max_length=30)),
                ('family_name', models.CharField(max_length=30)),
                ('can_buy', models.BooleanField()),
                ('can_sell', models.BooleanField()),
                ('location', models.CharField(max_length=100)),
                ('diet_reqs', models.ManyToManyField(to='MealSharing.contains')),
                ('rating', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MealSharing.rating')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='meal',
            name='buyer',
        ),
        migrations.AlterField(
            model_name='meal',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='meal',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MealSharing.order'),
        ),
    ]
