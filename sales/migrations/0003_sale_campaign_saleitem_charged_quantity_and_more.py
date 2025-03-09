# Generated by Django 5.1.6 on 2025-02-16 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
        ('sales', '0002_rename_price_per_item_saleitem_unit_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='campaign',
            field=models.ForeignKey(blank=True, help_text='Campaign applied to the sale (if applicable)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaigns.campaign'),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='charged_quantity',
            field=models.PositiveIntegerField(default=0, editable=False, help_text='Effective quantity charged (computed)'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, help_text='Quantity scanned/entered'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, editable=False, help_text='Base price of the product variant', max_digits=10),
        ),
    ]
