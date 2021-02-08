# Generated by Django 3.1.5 on 2021-01-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_articlecategory_userarticlecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]