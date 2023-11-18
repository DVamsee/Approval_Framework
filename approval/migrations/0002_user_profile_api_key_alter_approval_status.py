# Generated by Django 4.2.7 on 2023-11-18 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='api_key',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='approval',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], max_length=20),
        ),
    ]