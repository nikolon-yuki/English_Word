# Generated by Django 3.2.7 on 2021-09-29 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0002_card_checkbox_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='checkbox_1',
            field=models.CharField(default='checked', max_length=10),
        ),
    ]
