# Generated by Django 4.1.4 on 2022-12-25 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_alter_note_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notes.folder'),
        ),
    ]