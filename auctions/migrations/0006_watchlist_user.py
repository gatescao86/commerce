# Generated by Django 5.0.6 on 2024-05-19 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]