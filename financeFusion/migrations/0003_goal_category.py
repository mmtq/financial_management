# Generated by Django 5.0.6 on 2024-06-25 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeFusion', '0002_goal_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financeFusion.category'),
        ),
    ]