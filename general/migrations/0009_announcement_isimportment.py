# Generated by Django 4.2.3 on 2023-08-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_alter_profile_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='isImportment',
            field=models.BooleanField(default=False),
        ),
    ]
