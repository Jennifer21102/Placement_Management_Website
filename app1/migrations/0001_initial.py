# Generated by Django 4.1 on 2022-11-05 06:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('logo', models.ImageField(default='', upload_to='app1/static/images')),
                ('spock_name', models.CharField(max_length=64)),
                ('spock_email', models.EmailField(max_length=254)),
                ('spock_phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('username', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('register_no', models.CharField(max_length=8)),
                ('phone_no', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('gender', models.CharField(max_length=8)),
                ('year_of_graduation', models.IntegerField()),
                ('combination', models.CharField(max_length=8)),
                ('marks10th', models.IntegerField()),
                ('marks12th', models.IntegerField()),
                ('dob', models.DateField()),
                ('username', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('designation', models.CharField(max_length=64)),
                ('no_of_vaccancies', models.IntegerField()),
                ('job_type', models.CharField(max_length=10)),
                ('mode_of_work', models.CharField(max_length=16)),
                ('qualifications', models.CharField(max_length=64)),
                ('year_of_graduation', models.IntegerField()),
                ('discipline_required', models.CharField(max_length=64)),
                ('eligibility', models.CharField(max_length=64)),
                ('bond_contract', models.CharField(max_length=64)),
                ('ctc_pa', models.CharField(max_length=8)),
                ('last_date', models.DateField()),
                ('shortlist', models.BooleanField()),
                ('written_test', models.BooleanField()),
                ('gd', models.BooleanField()),
                ('interview', models.BooleanField()),
                ('no_of_rounds', models.IntegerField()),
                ('extra_comments', models.CharField(max_length=16)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Offers', to='app1.company')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=1)),
                ('resume', models.FileField(upload_to='app1/static/student-resume/')),
                ('aggregate', models.IntegerField()),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Application', to='app1.offer')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Application', to='app1.student')),
            ],
        ),
    ]
