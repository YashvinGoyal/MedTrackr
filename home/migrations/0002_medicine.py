# Generated by Django 4.1 on 2023-06-27 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='medicine',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('nameM', models.CharField(max_length=20)),
                ('doses', models.TextField(max_length=10)),
                ('frequency', models.TextField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
