# Generated by Django 2.0.4 on 2018-04-29 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicequestion',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.Choice'),
        ),
    ]
