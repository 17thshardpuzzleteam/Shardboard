# Generated by Django 3.2.18 on 2024-10-09 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('marker', models.CharField(max_length=7, verbose_name='Marker')),
                ('category_id', models.IntegerField(unique=True, verbose_name='Round Category ID')),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='hunt',
            name='unique_guild_name_combination',
        ),
        migrations.AddConstraint(
            model_name='hunt',
            constraint=models.UniqueConstraint(fields=('guild_id', 'category_id'), name='unique_guild_hunt_category_combination'),
        ),
        migrations.AddField(
            model_name='round',
            name='hunt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hunts.hunt'),
        ),
    ]
