# Generated by Django 3.0.3 on 2020-03-31 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_item', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_item.Company'),
        ),
        migrations.AlterField(
            model_name='item',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_item.Department'),
        ),
    ]
