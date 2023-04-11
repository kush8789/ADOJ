# Generated by Django 4.2 on 2023-04-11 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50)),
                ('difficulty', models.CharField(choices=[('Easy', 'easy'), ('Medium', 'medium'), ('Hard', 'hard')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.CharField(max_length=50)),
                ('output', models.CharField(max_length=50)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.problem')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verdict', models.CharField(max_length=50)),
                ('submittedAt', models.DateTimeField(auto_now=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.problem')),
            ],
        ),
    ]