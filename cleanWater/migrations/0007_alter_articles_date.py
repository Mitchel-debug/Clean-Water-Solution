# Generated by Django 4.0.4 on 2022-11-02 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleanWater', '0006_alter_articles_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
