# Generated by Django 3.2.14 on 2022-08-15 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.DateField(null=True, verbose_name='date published'),
        ),
    ]
