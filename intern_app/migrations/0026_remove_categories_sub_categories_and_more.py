# Generated by Django 5.1.7 on 2025-04-04 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_app', '0025_alter_categories_sub_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='sub_categories',
        ),
        migrations.AddField(
            model_name='categories',
            name='sub_categories',
            field=models.ManyToManyField(blank=True, related_name='parent_categories', to='intern_app.categories', verbose_name='Kategori Türü'),
        ),
    ]
