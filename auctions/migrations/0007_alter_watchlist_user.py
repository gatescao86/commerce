# Generated by Django 5.0.6 on 2024-05-20 07:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_watchlist_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="watchlist",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
