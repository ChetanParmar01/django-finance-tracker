# Generated by Django 4.2.21 on 2025-06-17 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_goal_current_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
