# Generated by Django 3.1.5 on 2021-01-28 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20210127_1114'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArticleCategory',
            new_name='Category',
        ),
    ]