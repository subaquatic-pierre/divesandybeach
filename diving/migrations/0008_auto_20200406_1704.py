# Generated by Django 3.0.2 on 2020-04-06 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diving', '0007_auto_20200406_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='divebookingrequest',
            options={'verbose_name_plural': 'Dive Bookings'},
        ),
        migrations.AlterModelOptions(
            name='divebookingrequestdiver',
            options={'verbose_name_plural': 'Divers Dive Booking'},
        ),
        migrations.RemoveField(
            model_name='coursebookingrequest',
            name='extra_divers',
        ),
        migrations.CreateModel(
            name='CourseBookingExtraDivers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('course_booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_divers', to='diving.CourseBookingRequest')),
            ],
        ),
    ]
