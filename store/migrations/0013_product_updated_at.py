# Generated by Django 5.1.1 on 2024-10-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_shoporder_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]