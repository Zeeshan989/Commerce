# Generated by Django 4.2.1 on 2023-05-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('biduid', models.CharField(max_length=65)),
                ('bpid', models.IntegerField()),
            ],
        ),
    ]
