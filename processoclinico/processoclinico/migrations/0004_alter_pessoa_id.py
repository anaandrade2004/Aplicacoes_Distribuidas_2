# Generated by Django 5.0.1 on 2025-01-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processoclinico', '0003_remove_pessoa_cc_remove_pessoa_nif_alter_stock_s_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False),
        ),
    ]
