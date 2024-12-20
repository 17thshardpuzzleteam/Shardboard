# Generated by Django 3.2.18 on 2024-10-10 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0002_auto_20241009_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=511, verbose_name='Name')),
                ('channel_id', models.IntegerField(verbose_name='Channel ID')),
                ('voice_channel_id', models.IntegerField(null=True, verbose_name='Voice Channel ID')),
                ('answer', models.CharField(max_length=255, null=True, verbose_name='Answer')),
                ('spreadsheet_link', models.CharField(max_length=255, verbose_name='Spreadsheet Link')),
                ('priority', models.CharField(max_length=15, verbose_name='Priority')),
                ('notes', models.CharField(max_length=511, null=True, verbose_name='Notes')),
                ('unlock_time', models.DateTimeField(verbose_name='Unlock Time')),
                ('solve_time', models.DateTimeField(null=True, verbose_name='Solve Time')),
                ('is_meta', models.BooleanField(default=False, verbose_name='Is Meta?')),
            ],
        ),
        migrations.AlterField(
            model_name='round',
            name='category_id',
            field=models.IntegerField(verbose_name='Round Category ID'),
        ),
        migrations.AddConstraint(
            model_name='round',
            constraint=models.UniqueConstraint(fields=('hunt', 'name'), name='unique_hunt_round_combination'),
        ),
        migrations.AddConstraint(
            model_name='round',
            constraint=models.UniqueConstraint(fields=('hunt', 'marker'), name='unique_hunt_marker_combination'),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='hunt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hunts.hunt'),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='metas',
            field=models.ManyToManyField(to='hunts.Puzzle'),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='rounds',
            field=models.ManyToManyField(to='hunts.Round'),
        ),
        migrations.AddConstraint(
            model_name='puzzle',
            constraint=models.UniqueConstraint(fields=('hunt', 'name'), name='unique_hunt_puzzle_combination'),
        ),
    ]
