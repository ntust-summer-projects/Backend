# Generated by Django 4.2.3 on 2023-07-29 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_component_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='material',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='material',
            name='EName',
        ),
    ]
