# Generated by Django 4.2 on 2024-06-07 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_invoice_paid_alter_brand_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='invoice',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Pagada'),
        ),
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
    ]
