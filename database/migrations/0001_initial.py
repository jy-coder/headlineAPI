# Generated by Django 2.1.15 on 2021-03-08 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=1000)),
                ('link', models.CharField(blank=True, max_length=1000)),
                ('summary', models.CharField(blank=True, max_length=3000)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.TextField(blank=True)),
                ('keywords', models.CharField(blank=True, max_length=3000)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('source', models.CharField(blank=True, max_length=100)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Article',
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('bookmark_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Article')),
            ],
            options={
                'db_table': 'Bookmark',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('category_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='ReadingHistory',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('history_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Article')),
            ],
            options={
                'db_table': 'ReadingHistory',
            },
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('recommend_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('recommend_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Article')),
            ],
            options={
                'db_table': 'Recommend',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('subscription_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Category')),
            ],
            options={
                'db_table': 'Subscription',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.CharField(default='', max_length=100, unique=True)),
                ('email', models.CharField(max_length=1000, unique=True)),
                ('full_name', models.CharField(max_length=1000)),
                ('last_active', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.AlterIndexTogether(
            name='user',
            index_together={('email',)},
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.User'),
        ),
        migrations.AddField(
            model_name='recommend',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.User'),
        ),
        migrations.AddField(
            model_name='readinghistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.User'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.User'),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('user', 'category')},
        ),
        migrations.AlterUniqueTogether(
            name='recommend',
            unique_together={('user', 'article')},
        ),
        migrations.AlterUniqueTogether(
            name='readinghistory',
            unique_together={('user', 'article')},
        ),
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together={('user', 'article')},
        ),
    ]
