# Generated by Django 3.0.2 on 2020-02-13 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diving', '0006_course_info_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemprice',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='diving.DiveTrip'),
        ),
    ]
