# Generated by Django 5.1.6 on 2025-03-12 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField(null=True)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('product_image', models.ImageField(upload_to='products/')),
            ],
            options={
                'verbose_name': 'Ürün',
                'verbose_name_plural': 'Ürünler',
            },
        ),
    ]
