# Generated by Django 3.0.2 on 2020-02-10 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diving', '0005_course_overview_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='info_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='info_image', to='diving.Images'),
        ),
    ]
