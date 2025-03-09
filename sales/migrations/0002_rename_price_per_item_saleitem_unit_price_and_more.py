# Generated by Django 5.1.6 on 2025-02-16 21:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saleitem',
            old_name='price_per_item',
            new_name='unit_price',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='campaign_applied',
        ),
        migrations.AddField(
            model_name='saleitem',
            name='campaign',
            field=models.ForeignKey(blank=True, help_text='Campaign applied to this sale item, if any', null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaigns.campaign'),
        ),
    ]
