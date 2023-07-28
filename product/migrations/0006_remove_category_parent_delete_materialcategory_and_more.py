# Generated by Django 4.2.3 on 2023-07-28 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_tag_remove_product_category_product_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.DeleteModel(
            name='MaterialCategory',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
        migrations.RemoveField(
            model_name='material',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
