# Migration: Add slug field to Product model
# Also updates Meta ordering for Category, ContactInquiry, Testimonial

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        # Add slug field to Product (nullable initially so existing rows don't break)
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, blank=True, null=True),
        ),

        # Update Meta options for Category
        migrations.AlterModelOptions(
            name='category',
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),

        # Update Meta options for ContactInquiry
        migrations.AlterModelOptions(
            name='contactinquiry',
            options={
                'verbose_name_plural': 'Contact Inquiries',
                'ordering': ['-created_at'],
            },
        ),

        # Update Meta options for Testimonial
        migrations.AlterModelOptions(
            name='testimonial',
            options={
                'ordering': ['-rating', 'author'],
            },
        ),

        # Update Meta options for Product
        migrations.AlterModelOptions(
            name='product',
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
