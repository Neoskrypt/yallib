# Generated by Django 2.0.5 on 2018-06-11 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yallib', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(choices=[('0', 'BLOCKED'),  ('1', 'ACTIVE'), ('2', 'DELETED'), ('3', 'SUSPENDED')], default=0),
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('first_name', 'last_name', 'date_birth')},
        ),
    ]