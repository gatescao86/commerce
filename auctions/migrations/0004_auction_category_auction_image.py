# Generated by Django 5.0.6 on 2024-05-19 03:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_auction_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction",
            name="category",
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name="auction",
            name="image",
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
