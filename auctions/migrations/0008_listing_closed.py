# Generated by Django 4.2.1 on 2023-05-31 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_commentcontent_userc'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.CharField(default='', max_length=65),
        ),
    ]
