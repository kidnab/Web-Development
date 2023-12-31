# Generated by Django 5.0 on 2023-12-17 07:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_category_listing"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="imageURL",
            new_name="imageurl",
        ),
        migrations.AddField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
