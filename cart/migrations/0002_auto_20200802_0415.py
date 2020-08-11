# Generated by Django 3.0.6 on 2020-08-02 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='replies', to='cart.Comment'),
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
