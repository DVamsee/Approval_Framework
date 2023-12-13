# Generated by Django 4.2.7 on 2023-11-22 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0007_alter_approval_approval_type_alter_approval_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='approval_type',
            field=models.CharField(choices=[('small', 'small'), ('adhoc', 'adhoc'), ('urgent', 'urgent')], max_length=20),
        ),
        migrations.AlterField(
            model_name='approval',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], max_length=20),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='role',
            field=models.CharField(choices=[('client', 'client'), ('admin', 'admin'), ('staff', 'staff')], max_length=50),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='approval.user_profile')),
            ],
        ),
    ]