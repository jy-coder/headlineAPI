# Generated by Django 3.1.5 on 2021-02-19 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_recommend_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommend',
            name='category',
        ),
    ]