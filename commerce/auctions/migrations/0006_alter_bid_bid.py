# Generated by Django 5.0 on 2024-01-19 19:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_bid_alter_listing_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="bid",
            field=models.IntegerField(),
        ),
    ]