# Generated by Django 4.1 on 2023-06-27 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_medicine'),
    ]

    operations = [
        migrations.CreateModel(
            name='doc',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('nam', models.CharField(max_length=100)),
            ],
        ),
    ]
