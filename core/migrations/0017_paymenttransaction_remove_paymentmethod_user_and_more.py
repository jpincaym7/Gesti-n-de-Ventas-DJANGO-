# Generated by Django 4.2 on 2024-06-07 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_creditcard_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='user',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='invoice',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='CreditCard',
        ),
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
        migrations.AddField(
            model_name='paymenttransaction',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_transactions', to='core.invoice'),
        ),
    ]
