# Generated by Django 3.0.2 on 2020-02-13 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diving', '0007_auto_20200213_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemprice',
            name='dive_trip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='diving.DiveTrip'),
        ),
        migrations.AlterField(
            model_name='itemprice',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='diving.Course'),
        ),
    ]