import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_order_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.shop'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.shop'),
        ),
    ]
