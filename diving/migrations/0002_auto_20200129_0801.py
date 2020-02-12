# Generated by Django 3.0.2 on 2020-01-29 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diving', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiveBookingRequestDiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('cert_level', models.CharField(blank=True, choices=[('Discover Scuba Diver', 'Discover Scuba Diver'), ('Junior Scuba Diver', 'Junior Scuba Diver'), ('Open Water', 'Open Water'), ('Advanced Open Water', 'Advanced Open Water'), ('Rescue Diver', 'Rescue Diver'), ('Deep Specialty', 'Deep Specialty')], max_length=255, null=True)),
                ('kit_required', models.CharField(blank=True, choices=[('FK', 'Full Kit'), ('TW', 'Tanks and Weights'), ('EXCL', 'Excluding Equipment')], max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='divebookingrequest',
            name='cert_level',
        ),
        migrations.AddField(
            model_name='coursebookingrequest',
            name='extra_divers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='ExtraDiver',
        ),
        migrations.AddField(
            model_name='divebookingrequestdiver',
            name='dive_booking_query',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extra_diver', to='diving.CourseBookingRequest'),
        ),
    ]
