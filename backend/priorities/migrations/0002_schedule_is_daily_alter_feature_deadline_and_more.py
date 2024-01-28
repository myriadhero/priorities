# Generated by Django 5.0.1 on 2024-01-28 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('priorities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='is_daily',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='feature',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='weekday',
            field=models.IntegerField(blank=True, choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.CheckConstraint(check=models.Q(('is_daily', True), ('weekday__isnull', False), _connector='OR'), name='daily_or_weekday', violation_error_message='Schedule must be either daily or on a specific weekday.'),
        ),
    ]