# Generated by Django 4.2.7 on 2023-11-28 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0009_alter_approval_approval_type_alter_approval_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflowstep',
            name='users',
            field=models.JSONField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='approval',
            name='approval_type',
            field=models.CharField(choices=[('small', 'small'), ('urgent', 'urgent'), ('adhoc', 'adhoc')], max_length=20),
        ),
        migrations.AlterField(
            model_name='approval',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=20),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('client', 'client'), ('staff', 'staff')], max_length=50),
        ),
    ]
