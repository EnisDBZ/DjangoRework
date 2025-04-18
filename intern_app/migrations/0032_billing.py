# Generated by Django 5.1.7 on 2025-04-11 10:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_app', '0031_alter_products_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('telno', models.CharField(max_length=11)),
                ('city', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=5)),
                ('address', models.CharField(max_length=300)),
                ('pay_method', models.CharField(max_length=255)),
                ('card_no', models.CharField(max_length=16)),
                ('card_exp', models.CharField(max_length=5)),
                ('card_owner', models.CharField(max_length=255)),
                ('card_cvv', models.CharField(max_length=3)),
                ('pay_id', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(choices=[('Bekliyor', 'Bekliyor'), ('Yola Çıktı', 'Yola Çıktı'), ('Tamamlandı', 'Tamamlandı')], default='Bekliyor', max_length=150)),
                ('message', models.TextField(null=True)),
                ('tracking_no', models.CharField(max_length=150, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
        ),
    ]
