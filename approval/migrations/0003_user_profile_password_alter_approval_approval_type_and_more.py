# Generated by Django 4.2.7 on 2023-11-19 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0002_user_profile_api_key_alter_approval_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='password',
            field=models.CharField(default='dlvgh123', max_length=50),
        ),
        migrations.AlterField(
            model_name='approval',
            name='approval_type',
            field=models.CharField(choices=[('urgent', 'urgent'), ('adhoc', 'adhoc'), ('small', 'small')], max_length=20),
        ),
        migrations.AlterField(
            model_name='approval',
            name='status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('approved', 'Approved'), ('pending', 'Pending')], max_length=20),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='role',
            field=models.CharField(choices=[('client', 'client'), ('admin', 'admin'), ('staff', 'staff')], max_length=50),
        ),
    ]
