# Generated by Django 4.2.3 on 2023-07-04 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientvisit',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='doctor_patients', to='doctor.doctor'),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='patient_visits', to='patient.patient'),
        ),
    ]