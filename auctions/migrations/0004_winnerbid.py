# Generated by Django 4.2.1 on 2023-05-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_bid_bid_bd'),
    ]

    operations = [
        migrations.CreateModel(
            name='winnerbid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(default=0)),
                ('winnerbid', models.CharField(default='temp', max_length=65)),
            ],
        ),
    ]
